from fastapi import FastAPI, HTTPException
from IPython import get_ipython
from .__version__ import __version__
from .search import search_online
from .config import get_config_manager, ConfigManager

__all__ = ['search_online', '__version__', 'setup_jupyter_whisper']
from anthropic.types import TextBlock
from IPython.core.magic import register_cell_magic
from IPython.display import display,  clear_output, Markdown
import time
import re
from .search import search_online
from IPython.display import Javascript
from ipylab import JupyterFrontEnd
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import os
import requests
import threading
import nest_asyncio
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import psutil
from contextlib import asynccontextmanager
from datetime import datetime
from io import StringIO
import sys

# Get model from config
config_manager = get_config_manager()
model = config_manager.get_model()

# Add debug flag at the top with other imports
DEBUG = False  # Set this to True to enable debug output

# Add OpenAI client initialization
config_manager = get_config_manager()
missing_keys = config_manager.ensure_api_keys()
if missing_keys:
    print(f"Warning: Missing API keys: {', '.join(missing_keys)}")
    print("Run setup_jupyter_whisper() to configure your API keys.")

# Modify OpenAI client initialization to be lazy-loaded
client = None  # Initialize as None initially


def get_openai_client():
    global client
    if client is None:
        config_manager = get_config_manager()
        if config_manager.get_api_key('OPENAI_API_KEY'):
            client = OpenAI()  # Will use OPENAI_API_KEY from environment/config
        else:
            print(
                "Warning: OpenAI API key not configured. Audio transcription will be unavailable.")
            print("Run setup_jupyter_whisper() to configure your API keys.")
    return client


# Add global variable to store outputs
cell_outputs = []  # List to store outputs
output_catcher = None  # Global variable to hold the OutputCatcher instance


class OutputCatcher:
    def __init__(self):
        self.stdout = StringIO()
        self.stderr = StringIO()
        self._stdout = sys.stdout
        self._stderr = sys.stderr

    def __enter__(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        return self

    def __exit__(self, *args):
        sys.stdout = self._stdout
        sys.stderr = self._stderr

    def get_output(self):
        return {
            'stdout': self.stdout.getvalue(),
            'stderr': self.stderr.getvalue()
        }


def create_assistant_cell():
    a = get_ipython()
    last_response = c.h[-1]['content']

    # Handle Claude 3 response format
    if isinstance(last_response, list):
        last_response = '\n'.join(block.text for block in last_response
                                if hasattr(block, 'text'))

    # Handle Claude 3 format in previous messages too
    if len(c.h) > 1:
        prev_content = c.h[-2]['content']
        if isinstance(prev_content, list):
            prev_content = '\n'.join(block.text for block in prev_content
                                   if hasattr(block, 'text'))
            c.h[-2]['content'] = prev_content

    # Clear cell outputs from the last user message
    if len(c.h) > 1 and isinstance(c.h[-2]['content'], str):
        c.h[-2]['content'] = re.sub(r'<cell_outputs>.*</cell_outputs>',
                                    '', c.h[-2]['content'])

    # Function to split code blocks from the assistant's response
    def split_code_blocks(text):
        parts = []
        current_part = ""
        in_code_block = False
        code_lang = None
        i = 0

        while i < len(text):
            # Check for escaped backticks
            if text[i:i+4] == '\\```':
                current_part += '```'
                i += 4
                continue

            # Check for commented backticks
            is_commented = False
            if i > 0:
                line_start = text.rfind('\n', 0, i)
                if line_start == -1:
                    line_start = 0
                line_prefix = text[line_start:i].lstrip()
                is_commented = line_prefix.startswith(
                    '#') or line_prefix.startswith('//')

            # Start of code block
            if text[i:i+3] == '```' and not in_code_block and not is_commented:
                if current_part.strip():
                    parts.append(current_part)
                current_part = text[i:i+3]
                i += 3
                # Language identifier
                lang_end = text.find('\n', i)
                if lang_end != -1:
                    code_lang = text[i:lang_end].strip()
                    current_part += code_lang + '\n'
                    i = lang_end + 1
                in_code_block = True
            # End of code block
            elif text[i:i+3] == '```' and in_code_block:
                current_part += text[i:i+3]
                parts.append(current_part)
                current_part = ""
                in_code_block = False
                code_lang = None
                i += 3
            else:
                current_part += text[i]
                i += 1

        if current_part.strip():
            parts.append(current_part)

        return parts

    parts = split_code_blocks(last_response)

    app = JupyterFrontEnd()

    count = 0
    for i, part in enumerate(parts):
        if part.strip():
            if part.lstrip().startswith('```'):
                # Handle code block
                code_content = part
                if code_content.startswith('```python'):
                    # Remove language identifier and closing backticks
                    code_content = code_content.replace(
                        '```python\n', '', 1).replace('```', '')
                    code_content = f"\n#%%assistant {len(c.h)-1}\n{code_content}"
                else:
                    # Handle other languages
                    match = re.match(r'```(\w+)\n', code_content)
                    if match:
                        lang = match.group(1)
                        lang = 'R' if lang.lower() == 'r' else lang
                        code_content = re.sub(
                            r'```\w+\n', '', code_content, 1).replace('```', '')
                        code_content = f"%%{lang}\n#%%assistant {len(c.h)-1}\n{code_content}"

                # Insert code cell
                if count == 0:
                    app.commands.execute('notebook:insert-cell-above')
                    time.sleep(0.2)
                    count += 1
                else:
                    app.commands.execute('notebook:insert-cell-below')
                    time.sleep(0.3)
                    count += 1
                app.commands.execute(
                    'notebook:replace-selection', {'text': code_content})
            else:
                # Handle markdown content
                markdown_content = f"%%assistant {len(c.h)-1}\n\n{part}\n"
                if count == 0:
                    app.commands.execute('notebook:insert-cell-above')
                    time.sleep(0.1)
                    count += 1
                else:
                    app.commands.execute('notebook:insert-cell-below')
                    time.sleep(0.3)
                    count += 1
                app.commands.execute(
                    'notebook:replace-selection', {'text': markdown_content})
                app.commands.execute('notebook:change-cell-to-markdown')
                app.commands.execute('notebook:run-cell')

            time.sleep(0.4)
            app.commands.execute('notebook:scroll-cell-center')

    # Create the next user cell
    app.commands.execute('notebook:insert-cell-below')
    time.sleep(0.2)
    app.commands.execute('notebook:replace-selection',
                         {'text': f"%%user {len(c.h)}\n\n"})
    app.commands.execute('notebook:scroll-cell-center')


def go(cell):
    # Replace empty cell or whitespace-only cell with 'continue'
    if not cell or cell.isspace():
        cell = 'continue'

    # Process expressions within {}
    pattern = r'\{([^}]+)\}'

    def eval_match(match):
        expr = match.group(1)
        try:
            shell = get_ipython()
            result = eval(expr, shell.user_ns)
            return str(result)
        except Exception as e:
            return f"[Error: {str(e)}]"

    cell = re.sub(pattern, eval_match, cell)
    app = JupyterFrontEnd()
    words = 0
    text = ""
    for word_piece in c(cell + f"""<cell_outputs> In here you have all the current jupyter context that we run so far. Use judiciously. {cell_outputs}</cell_outputs>""", stream=True):
        words += 1
        # Handle Claude 3 response format
        if isinstance(word_piece, (list, TextBlock)):
            text += word_piece.text if hasattr(word_piece, 'text') else ''
        else:
            text += word_piece
        if words % 20 == 0:
            clear_output(wait=False)
            display(Markdown(text))
            app.commands.execute('notebook:scroll-cell-center')
    clear_output(wait=False)
    create_assistant_cell()


@register_cell_magic
def user(line, cell):
    global c
    parts = line.split(':')
    index = int(parts[0]) if parts[0] else len(c.h)
    action = parts[1] if len(parts) > 1 else None

    if index == 0:
        config_manager = get_config_manager()
        # Use the globally defined Chat class
        c = globals()['Chat'](config_manager.get_model(),
                    sp=config_manager.get_system_prompt())
        # Update c in user's namespace when reset
        get_ipython().user_ns['c'] = c

    if action == 'set':
        # Set the content without running or creating next cell
        if index < len(c.h):
            c.h[index] = {'role': 'user', 'content': cell}
        else:
            c.h.append({'role': 'user', 'content': cell})
        return  # Early return

    if index < len(c.h):
        if action == 'wipe':
            c.h = c.h[:index]
            go(cell)
        else:
            c.h[index] = {'role': 'user', 'content': cell}
            go(cell)
    else:
        go(cell)


@register_cell_magic
def assistant(line, cell):
    parts = line.split(':')
    index_str = parts[0]
    action = parts[1] if len(parts) > 1 else None

    # Parse main index
    main_index = int(index_str) if index_str else len(c.h) - 1

    if action == 'add':
        # For add action, concatenate with existing content
        if main_index < len(c.h):
            existing_content = c.h[main_index].get('content', '')
            if isinstance(existing_content, list):
                # Handle Claude 3 format - convert to string first
                existing_content = '\n'.join(block.text for block in existing_content
                                          if hasattr(block, 'text'))

            # Add a newline between existing and new content if both exist
            separator = '\n' if existing_content and cell else ''
            new_content = existing_content + separator + cell

            # Update the content
            c.h[main_index]['content'] = new_content
        else:
            # Append new entry if index doesn't exist
            c.h.append({'role': 'assistant', 'content': cell})
        return  # Early return

    elif action == 'set':
        # For set action, completely replace the content
        if main_index < len(c.h):
            c.h[main_index]['content'] = cell
        else:
            c.h.append({'role': 'assistant', 'content': cell})
        return  # Early return

    # Rest of the function remains unchanged...


a = get_ipython()
# Load R and Julia extensions if available
try:
    a.run_line_magic('load_ext', 'rpy2.ipython')
except:
    pass
try:
    a.run_line_magic('load_ext', 'sql')
except:
    pass

a.set_next_input("%%user 0\n\n", replace=False)


ip = get_ipython()


def determine_cell_type(raw_cell):
    """Determine the cell type based on content"""
    if not raw_cell:
        return 'unknown'

    # Check for magic commands
    if raw_cell.startswith('%%'):
        magic_type = raw_cell[2:].split('\n')[0].strip()
        return f'magic_{magic_type}'

    # Check for markdown cells (usually start with #, >, or contain markdown syntax)
    if raw_cell.lstrip().startswith(('#', '>', '-', '*', '```')):
        return 'markdown'

    # Check if it's mostly code
    code_indicators = ['def ', 'class ', 'import ',
        'from ', 'print(', 'return ', '    ']
    if any(indicator in raw_cell for indicator in code_indicators):
        return 'code'

    return 'text'


def pre_run_cell(info):
    global output_catcher
    output_catcher = OutputCatcher()
    output_catcher.__enter__()  # Start capturing


def post_run_cell(result):
    global cell_outputs, output_catcher

    # Finish capturing
    if output_catcher is not None:
        output_catcher.__exit__()
        outputs = output_catcher.get_output()
        output_catcher = None
    else:
        outputs = {'stdout': '', 'stderr': ''}

    # Get raw cell content
    raw_cell = getattr(result.info, 'raw_cell', '')
    exec_count = getattr(result.info, 'execution_count', None)

    # Initialize output data
    output_data = {
        'execution_count': exec_count,
        'input': raw_cell,
        'output': None,
        'stdout': outputs['stdout'],
        'stderr': outputs['stderr'],
        'error': None,
        'timestamp': datetime.now(),
        'type': determine_cell_type(raw_cell)
    }

    # Display captured stdout/stderr immediately if not empty
    if outputs['stdout']:
        print(outputs['stdout'], end='')
    if outputs['stderr']:
        print(outputs['stderr'], file=sys.stderr, end='')

    # Check for errors
    if hasattr(result, 'error_in_exec') and result.error_in_exec is not None:
        output_data['error'] = str(result.error_in_exec)
        if hasattr(result, 'traceback'):
            output_data['stderr'] += '\n'.join(result.traceback)

    # Get the result of the cell execution
    if hasattr(result, 'result') and result.result is not None:
        output_data['output'] = str(result.result)

    # Collect display outputs
    if hasattr(result, 'display_outputs'):
        for display_output in result.display_outputs:
            if display_output.output_type == 'stream':
                if display_output.name == 'stdout':
                    output_data['stdout'] += display_output.text
                elif display_output.name == 'stderr':
                    output_data['stderr'] += display_output.text
            elif display_output.output_type == 'error':
                output_data['error'] = display_output.evalue
                output_data['stderr'] += '\n'.join(display_output.traceback)
            elif display_output.output_type == 'execute_result':
                if 'text/plain' in display_output.data:
                    output_data['output'] = display_output.data['text/plain']
            elif display_output.output_type == 'display_data':
                # Handle outputs from magic commands like %%bash
                if 'text/plain' in display_output.data:
                    output_data['stdout'] += display_output.data['text/plain']
                elif 'text/html' in display_output.data:
                    output_data['stdout'] += display_output.data['text/html']

    # Append to cell_outputs
    if raw_cell.strip():
        cell_outputs.append(output_data)

    # Debug logging
    if DEBUG:
        print(f"Captured output for cell type {output_data['type']}:")
        print(f"stdout: {output_data['stdout']}")
        print(f"stderr: {output_data['stderr']}")
        print(f"output: {output_data['output']}")
        print(f"error: {output_data['error']}")


# Register the hooks
ip.events.register('pre_run_cell', pre_run_cell)
ip.events.register('post_run_cell', post_run_cell)


def hist():
    """Display the chat history in a nicely formatted markdown view"""
    history_md = "# 💬 Chat History\n\n"
    for i, msg in enumerate(c.h):
        role = msg['role'].title()

        # Handle different content structures
        if isinstance(msg['content'], list):
            # Handle list of content blocks (Claude 3 format)
            content = '\n'.join(block.text for block in msg['content']
                              if isinstance(block, TextBlock))
        else:
            # Handle direct string content
            content = msg['content']

        # Add emoji based on role
        emoji = "🤖" if role == "Assistant" else "👤"

        # Add message header with role and index
        history_md += f"### {emoji} {role} [{i}]\n\n"

        # Add message content with proper indentation
        content = content.strip()  # Remove extra whitespace
        history_md += f"{content}\n\n"

        # Add a subtle separator
        history_md += "<hr style='border-top: 1px solid #ccc'>\n\n"

    display(Markdown(history_md))


class TextRequest(BaseModel):
    selectedText: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if DEBUG:
        print("Server shutting down...")
    # Add any cleanup code here if needed

app = FastAPI(lifespan=lifespan)

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
    max_age=3600,  # Cache preflight requests for 1 hour
)


@app.post("/quick_edit")
async def quick_edit(request: TextRequest):
    if DEBUG:
        print(
            f"Received request with text length: {len(request.selectedText)}")

    config = get_config_manager()
    api_key = config.get_api_key('ANTHROPIC_API_KEY')

    if not api_key:
        raise HTTPException(
            status_code=400,
            detail="ANTHROPIC_API_KEY not found. Please run setup_jupyter_whisper() to configure."
        )

    url = 'https://api.anthropic.com/v1/messages'
    headers = {
        'x-api-key': api_key,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
    }

    # Get quick edit configurations
    quick_edit_model = config.get_config_value(
        'QUICK_EDIT_MODEL', 'claude-3-5-sonnet-20241022')
    quick_edit_system_prompt = config.get_config_value(
        'QUICK_EDIT_SYSTEM_PROMPT')

    data = {
        "model": quick_edit_model,
        "system": quick_edit_system_prompt,
        "messages": [
            {"role": "user", "content": request.selectedText}
        ],
        "max_tokens": 8192
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if DEBUG:
            print(f"HTTP Error: {str(e)}")
            print(f"Response content: {e.response.text}")
        raise HTTPException(
            status_code=500, detail=f"Anthropic API error: {str(e)}")
    except requests.exceptions.RequestException as e:
        if DEBUG:
            print(f"Request Error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Request failed: {str(e)}")
    except Exception as e:
        if DEBUG:
            print(f"Unexpected Error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/audio")
async def process_audio(audio: UploadFile = File(...)):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "*",
    }
    # Add debug logging
    if DEBUG:
        print("Audio processing request received")
        print(f"Current OpenAI client configuration:")
        print(
            f"- Environment key: {os.environ.get('OPENAI_API_KEY', 'Not set')[:8]}...")

    client = get_openai_client()
    if client is None:
        raise HTTPException(
            status_code=400,
            detail="OpenAI API key not configured. Please run setup_jupyter_whisper() first."
        )

    # More debug logging
    if DEBUG:
        print(f"OpenAI client initialized with key: {client.api_key[:8]}...")

    # List of supported audio formats
    SUPPORTED_FORMATS = ['flac', 'm4a', 'mp3', 'mp4',
        'mpeg', 'mpga', 'oga', 'ogg', 'wav', 'webm']

    try:
        # Check file extension
        file_extension = audio.filename.split('.')[-1].lower()
        if file_extension not in SUPPORTED_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Supported formats: {SUPPORTED_FORMATS}"
            )

        # Save the uploaded file temporarily
        temp_file_path = f"temp_{audio.filename}"
        with open(temp_file_path, "wb") as temp_file:
            contents = await audio.read()
            temp_file.write(contents)

        # Open and transcribe the audio file using Whisper
        with open(temp_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        if DEBUG:
            print(f"Transcript: {transcription}")

        # Clean up temporary file
        # os.remove(temp_file_path)

        # Return the actual transcription text
        return {"text": transcription}, headers

    except HTTPException as he:
        raise he
    except Exception as e:
        if DEBUG:
            print(f"Audio processing error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to process audio: {str(e)}")
    finally:
        # Ensure temp file is cleaned up even if an error occurs
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def shutdown_existing_server():
    if DEBUG:
        print("Checking for existing server on port 5000...")

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Get connections separately
            connections = proc.net_connections()
            for conn in connections:
                if hasattr(conn, 'laddr') and hasattr(conn.laddr, 'port') and conn.laddr.port == 5000:
                    if DEBUG:
                        print(f"Found process using port 5000: PID {proc.pid}")
                    proc.terminate()
                    proc.wait()  # Wait for the process to terminate
                    if DEBUG:
                        print("Successfully terminated existing server")
                    return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        except Exception as e:
            if DEBUG:
                print(f"Error checking process {proc.pid}: {e}")
            continue


def check_existing_server(port=5000, retries=3, delay=0.5):
    """Check if there's an existing server running with retries"""
    for attempt in range(retries):
        try:
            response = requests.get(
                f"http://localhost:{port}/status", timeout=1)
            if response.status_code == 200:
                # Verify it's our server by checking response format
                data = response.json()
                if "status" in data and "pid" in data:
                    if DEBUG:
                        print(
                            f"Found existing server on port {port} (PID: {data['pid']})")
                    return True
        except requests.exceptions.RequestException:
            if DEBUG and attempt == retries - 1:
                print(
                    f"No existing server found on port {port} after {retries} attempts")
            time.sleep(delay)
            continue
    return False


# Global flag to track server initialization
_server_initialized = False


def start_server_if_needed():
    """Start server only if no server is running"""
    global _server_initialized

    # Prevent multiple initialization attempts
    if _server_initialized:
        return

    try:
        response = requests.get('http://localhost:5000/status', timeout=1)
        if response.status_code == 200:
            server_info = response.json()
            print(f"Using existing server (PID: {server_info.get('pid')})")
            if DEBUG:
                print(f"Server version: {server_info.get('version')}")
                print(
                    f"Memory usage: {server_info.get('memory_usage', 0):.2f} MB")
            _server_initialized = True
            return
    except requests.exceptions.RequestException:
        if DEBUG:
            print("No existing server found, starting new one...")

        # Start new server in a thread
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        # Wait for server to be ready
        for _ in range(5):  # Try 5 times
            time.sleep(1)  # Wait a bit between attempts
            try:
                requests.get('http://localhost:5000/status', timeout=1)
                _server_initialized = True
                return
            except requests.exceptions.RequestException:
                continue

        if DEBUG:
            print("Warning: Server may not have started properly")


def run_server():
    """Start the FastAPI server"""
    import asyncio
    from uvicorn.config import Config
    from uvicorn.server import Server

    if DEBUG:
        print("Starting FastAPI server on port 5000...")

    config = Config(
        app=app,
        host="0.0.0.0",
        port=5000,
        log_level="warning",  # Reduce logging noise
        timeout_keep_alive=30,
        limit_concurrency=100
    )

    server = Server(config=config)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    nest_asyncio.apply()

    try:
        loop.run_until_complete(server.serve())
    except Exception as e:
        if DEBUG:
            print(f"Server error: {e}")


# Initialize only once at import
start_server_if_needed()


@app.get("/status")
async def status():
    """Health check endpoint with server info"""
    return {
        "status": "ok",
        "pid": os.getpid(),
        "timestamp": time.time(),
        "version": __version__,
        "memory_usage": psutil.Process().memory_info().rss / 1024 / 1024  # MB
    }

# Add graceful shutdown handler


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on server shutdown"""
    if DEBUG:
        print("Server shutting down...")
    # Add any cleanup code here if needed

# Add this JavaScript injection function before the server startup


def inject_js():
    # First, inject cleanup code
    cleanup_js = """
    if (window.cleanupAllHandlers) {
        window.cleanupAllHandlers();
        console.log('Cleaned up existing handlers');
    }
    """
    display(Javascript(cleanup_js))

    # Then read and inject the main code
    try:
        import os
        import pkg_resources

        # Get the package's installed location
        static_dir = pkg_resources.resource_filename(
            'jupyter_whisper', 'static')

        # Ensure static directory exists
        os.makedirs(static_dir, exist_ok=True)

        # Define default JS content if files don't exist
        default_main_js = """// Default main.js content
console.log('Using default main.js content');
// Add your default main.js content here
"""
        default_voice_js = """// Default voicerecorder.js content
console.log('Using default voicerecorder.js content');
// Add your default voicerecorder.js content here
"""

        # Try to read files, use defaults if not found
        try:
            with open(os.path.join(static_dir, 'main.js'), 'r') as f:
                main_js = f.read()
        except FileNotFoundError:
            main_js = default_main_js

        try:
            with open(os.path.join(static_dir, 'voicerecorder.js'), 'r') as f:
                voice_js = f.read()
        except FileNotFoundError:
            voice_js = default_voice_js

        # Combine the JS code
        js_code = voice_js + "\n\n" + main_js

        # Replace debug value
        js_code = js_code.replace(
            '{debug_value}', 'true' if DEBUG else 'false')

        display(Javascript(js_code))

    except Exception as e:
        print(f"Warning: Error loading JavaScript files: {e}")
        print("Some features may be limited.")


# Modify the server startup section to include the JS injection
start_server_if_needed()
inject_js()


def setup_jupyter_whisper(force_display=False):
    try:
        import ipywidgets as widgets
        from IPython.display import display, HTML, clear_output

        config_manager = get_config_manager()

        # Global variables
        available_models_dict = config_manager.get_available_models()
        custom_providers = config_manager.get_custom_providers()
        profiles = config_manager.get_quick_edit_profiles()
        active_profile = config_manager.get_active_quick_edit_profile()
        profile_buttons = {}
        selected_provider = None

        # Event handler functions
        def update_model_options(*args):
            """Update model options in the Model tab when provider changes"""
            provider = provider_dropdown.value
            models = available_models_dict.get(provider, [])
            model_dropdown.options = models

            # Set default value safely
            if model_dropdown.value in models:
                # Keep current value
                pass
            elif models:
                model_dropdown.value = models[0]
            else:
                model_dropdown.value = None

        def update_profile_model_options(*args):
            """Update model options when provider changes in profile settings"""
            provider = profile_provider_dropdown.value
            available_models = available_models_dict.get(provider, [])
            profile_model_dropdown.options = available_models

            # Ensure the selected model is valid
            if profile_model_dropdown.value in available_models:
                # Keep current value
                pass
            elif available_models:
                profile_model_dropdown.value = available_models[0]
            else:
                profile_model_dropdown.value = None

        def update_profile_buttons():
            """Refresh profile buttons"""
            profile_buttons.clear()
            for profile_id, profile in profiles.items():
                btn = widgets.Button(
                    description=profile['name'],
                    layout=widgets.Layout(margin='2px'),
                    button_style='info' if profile_id == active_profile else ''
                )
                btn._profile_id = profile_id
                btn.on_click(on_profile_button_clicked)
                profile_buttons[profile_id] = btn
            profile_buttons_container.children = list(profile_buttons.values())

        def update_profile_ui(profile_id):
            """Update UI to reflect selected profile"""
            profile = profiles[profile_id]
            profile_name_input.value = profile['name']
            provider = profile.get('provider', 'anthropic')
            model = profile['model']

            # Set provider and update models
            profile_provider_dropdown.value = provider
            # This will automatically update the model options
            update_profile_model_options()
            # Set model
            if model in profile_model_dropdown.options:
                profile_model_dropdown.value = model
            elif profile_model_dropdown.options:
                profile_model_dropdown.value = profile_model_dropdown.options[0]
            else:
                profile_model_dropdown.value = None

            # Update system prompt
            profile_system_prompt.value = profile['system_prompt']

            # Update button styles
            for btn in profile_buttons.values():
                btn.button_style = 'info' if btn._profile_id == profile_id else ''

        def on_profile_button_clicked(b):
            """Handle profile button clicks"""
            profile_id = b._profile_id
            config_manager.set_active_quick_edit_profile(profile_id)
            profiles.update(config_manager.get_quick_edit_profiles())  # Refresh profiles data
            update_profile_ui(profile_id)

        def on_add_profile_clicked(b):
            """Handle adding new profile"""
            new_id = f"profile_{len(profiles)}"
            new_name = f"New Profile {len(profiles)}"
            config_manager.add_quick_edit_profile(
                new_id,
                new_name,
                profile_provider_dropdown.value,
                profile_model_dropdown.value,
                "Enter system prompt here..."
            )
            # Refresh UI
            profiles.update(config_manager.get_quick_edit_profiles())
            update_profile_buttons()
            # Set the new profile as active
            config_manager.set_active_quick_edit_profile(new_id)
            update_profile_ui(new_id)

        def on_delete_profile_clicked(b):
            """Handle deleting current profile"""
            current_profile = config_manager.get_active_quick_edit_profile()
            if current_profile != 'default':
                try:
                    config_manager.remove_quick_edit_profile(current_profile)
                    profiles.update(config_manager.get_quick_edit_profiles())
                    update_profile_buttons()
                    # Switch to default profile
                    config_manager.set_active_quick_edit_profile('default')
                    update_profile_ui('default')
                except Exception as e:
                    with status_output:
                        clear_output()
                        print(f"Error deleting profile: {str(e)}")

        def on_save_clicked(b):
            global c  # Access global variables
            with status_output:
                clear_output()
                try:
                    # Save API keys
                    for key_name, key_info in keys.items():
                        widget = key_info['widget']
                        value = widget.value.strip()
                        if value and key_info['validate'](value):
                            config_manager.set_api_key(key_name, value)

                    # Save provider and model selection in Model tab
                    if model_dropdown.value is None:
                        raise ValueError("Please select a valid model")

                    config_manager.set_model(
                        model=model_dropdown.value,
                        provider=provider_dropdown.value
                    )

                    # Save system prompt
                    config_manager.set_system_prompt(system_prompt.value)

                    # Save current profile changes
                    current_profile = config_manager.get_active_quick_edit_profile()
                    config_manager.add_quick_edit_profile(
                        current_profile,
                        profile_name_input.value,
                        profile_provider_dropdown.value,
                        profile_model_dropdown.value,
                        profile_system_prompt.value
                    )

                    # Save popup preference
                    config_manager.set_config_value('SKIP_SETUP_POPUP', skip_setup_checkbox.value)

                    # Update UI
                    update_profile_buttons()

                    print("\n✅ Configuration saved successfully!")
                    print("\n✅ Quick Edit profiles updated!")
                except Exception as e:
                    print(f"\n❌ Error saving configuration: {str(e)}")
            c = initialize_chat()

        def on_reset_prompts_clicked(b):
            with status_output:
                clear_output()
                # Reset system prompts to default
                default_system_prompt = config_manager.DEFAULT_CONFIG['system_prompt']
                default_quick_edit_profiles = config_manager.DEFAULT_CONFIG['preferences']['QUICK_EDIT_PROFILES']

                system_prompt.value = default_system_prompt
                # Reset each profile's system prompt
                for profile_id in profiles:
                    profiles[profile_id]['system_prompt'] = default_quick_edit_profiles[profile_id]['system_prompt']

                profile_system_prompt.value = profiles[active_profile]['system_prompt']

                print("System prompts have been reset to default values.")

        # Event handlers for custom providers
        def on_custom_provider_selected(change):
            """Update UI fields when a custom provider is selected."""
            provider_id = change['new']
            if provider_id and provider_id in custom_providers:
                provider_data = custom_providers[provider_id]
                provider_name_input.value = provider_id
                display_name_input.value = provider_data['name']
                models_input.value = ', '.join(provider_data['models'])
                initialization_code_input.value = provider_data['initialization_code']
            else:
                provider_name_input.value = ''
                display_name_input.value = ''
                models_input.value = ''
                initialization_code_input.value = ''

        def on_save_provider_clicked(b):
            """Save or update the custom provider."""
            provider_id = provider_name_input.value.strip()
            if not provider_id:
                with status_output:
                    clear_output()
                    print("Provider Name is required.")
                return
            display_name = display_name_input.value.strip() or provider_id
            models = [m.strip() for m in models_input.value.strip().split(',') if m.strip()]
            initialization_code = initialization_code_input.value.strip()

            try:
                # Validate the initialization code
                config_manager.validate_initialization_code(initialization_code)
                # Add or update the provider
                config_manager.add_custom_provider(
                    provider_id, display_name, models, initialization_code
                )
                # Refresh custom providers
                custom_providers.update(config_manager.get_custom_providers())
                # Update the provider dropdown
                provider_options = [(p['name'], name) for name, p in custom_providers.items()]
                custom_provider_dropdown.options = provider_options
                custom_provider_dropdown.value = provider_id
                with status_output:
                    clear_output()
                    print(f"Provider '{display_name}' saved successfully.")
                # Update models in other tabs
                available_models_dict.update(config_manager.get_available_models())
                update_model_options()
                update_profile_model_options()
            except Exception as e:
                with status_output:
                    clear_output()
                    print(f"Error saving provider: {str(e)}")

        def on_add_new_provider_clicked(b):
            """Clear input fields to add a new provider."""
            custom_provider_dropdown.value = None
            provider_name_input.value = ''
            display_name_input.value = ''
            models_input.value = ''
            initialization_code_input.value = ''

        def on_delete_provider_clicked(b):
            """Delete the selected custom provider."""
            provider_id = provider_name_input.value.strip()
            if not provider_id or provider_id not in custom_providers:
                with status_output:
                    clear_output()
                    print("No provider selected to delete.")
                return
            try:
                config_manager.remove_custom_provider(provider_id)
                custom_providers.update(config_manager.get_custom_providers())
                provider_options = [(p['name'], name) for name, p in custom_providers.items()]
                if provider_options:
                    custom_provider_dropdown.options = provider_options
                    custom_provider_dropdown.value = provider_options[0][1]
                else:
                    custom_provider_dropdown.options = [("No providers available", None)]
                    custom_provider_dropdown.value = None
                on_add_new_provider_clicked(None)  # Clear fields
                with status_output:
                    clear_output()
                    print(f"Provider '{provider_id}' deleted successfully.")
                # Update models in other tabs
                available_models_dict.update(config_manager.get_available_models())
                update_model_options()
                update_profile_model_options()
            except Exception as e:
                with status_output:
                    clear_output()
                    print(f"Error deleting provider: {str(e)}")

        # Check if setup should be skipped
        if not force_display and config_manager.get_config_value('SKIP_SETUP_POPUP', False):
            return

        # Create status output and buttons first
        status_output = widgets.Output()
        save_button = widgets.Button(
            description='Save Configuration',
            button_style='primary',
            icon='check'
        )
        reset_prompts_button = widgets.Button(
            description='Reset to Default Prompts',
            button_style='warning',
            icon='refresh'
        )
        skip_setup_checkbox = widgets.Checkbox(
            value=config_manager.get_config_value('SKIP_SETUP_POPUP', False),
            description='Don\'t show this setup popup on startup',
            indent=False,
            layout=widgets.Layout(margin='20px 0')
        )

        # Add collapsible container
        accordion = widgets.Accordion()
        main_container = widgets.VBox()

        # Style for the UI
        display(HTML("""
        <style>
            .widget-label { font-weight: bold; }
            .setup-header { 
                font-size: 1.2em; 
                margin-bottom: 1em; 
                padding: 0.5em;
                background: #f0f0f0;
                border-radius: 4px;
                color: black;
            }
            .key-status {
                margin-top: 0.5em;
                font-style: italic;
            }
            .section-header {
                font-weight: bold;
                margin-top: 1em;
                margin-bottom: 0.5em;
                padding: 0.3em;
                background: #e0e0e0;
                border-radius: 4px;
            }
            .profile-button {
                margin: 2px;
                min-width: 120px;
            }
            .active-profile {
                background-color: #007bff;
                color: white;
            }
        </style>
        """))

        # Create tabs for different settings
        tab = widgets.Tab()
        api_keys_tab = widgets.VBox()
        model_tab = widgets.VBox()
        system_prompt_tab = widgets.VBox()
        quick_edit_tab = widgets.VBox()
        custom_providers_tab = widgets.VBox()  # New tab

        # API Keys Section
        keys = {
            'OPENAI_API_KEY': {
                'display': 'OpenAI API Key (for audio transcription)',
                'validate': lambda x: x.startswith('sk-') and len(x) > 20,
                'widget': None
            },
            'ANTHROPIC_API_KEY': {
                'display': 'Anthropic API Key (for Claude)',
                'validate': lambda x: x.startswith(('sk-', 'ant-')) and len(x) > 20,
                'widget': None
            },
            'PERPLEXITY_API_KEY': {
                'display': 'Perplexity API Key (for online search)',
                'validate': lambda x: x.startswith('pplx-') and len(x) > 20,
                'widget': None
            }
        }

        # Include API keys for custom providers
        for provider_name, provider_info in custom_providers.items():
            key_name = f"{provider_name.upper()}_API_KEY"
            keys[key_name] = {
                'display': f'{provider_info["name"]} API Key',
                'validate': lambda x: len(x) > 0,  # Adjust validation as needed
                'widget': None
            }

        api_key_widgets = []
        for key_name, key_info in keys.items():
            current_value = config_manager.get_api_key(key_name)
            masked_value = f"{current_value[:8]}...{current_value[-4:]}" if current_value else ""

            key_input = widgets.Password(
                placeholder=f'Enter {key_info["display"]}',
                value=current_value or '',
                description=key_info['display'],
                style={'description_width': 'initial'},
                layout=widgets.Layout(width='80%')
            )

            keys[key_name]['widget'] = key_input
            api_key_widgets.append(key_input)
            if current_value:
                api_key_widgets.append(widgets.HTML(
                    f'<div class="key-status">Current value: {masked_value}</div>'
                ))

        api_keys_tab.children = api_key_widgets

        # Model Selection Section
        current_model, current_provider = config_manager.get_model()

        # Create provider dropdown
        provider_options = list(available_models_dict.keys())
        provider_dropdown = widgets.Dropdown(
            options=provider_options,
            value=current_provider,  # Set current provider as default
            description='Provider:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='50%')
        )

        # Create model dropdown
        model_dropdown = widgets.Dropdown(
            description='Model:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='50%')
        )

        # Initial update of model options
        update_model_options()

        # Link provider changes to model updates
        provider_dropdown.observe(update_model_options, names='value')

        # Assemble model tab
        model_tab.children = [
            widgets.HTML('<div class="section-header">Model Selection</div>'),
            provider_dropdown,
            model_dropdown,
            widgets.HTML('<div class="key-status">Select the provider and model to use for chat interactions.</div>')
        ]

        # System Prompt Section
        system_prompt = widgets.Textarea(
            value=config_manager.get_system_prompt(),
            placeholder='Enter system prompt...',
            description='System Prompt:',
            disabled=False,
            layout=widgets.Layout(width='95%', height='400px'),
            continuous_update=True  # Enable continuous updates
        )

        # Add keyboard handler for system prompt
        system_prompt._dom_classes = system_prompt._dom_classes + ('jp-mod-accept-enter',)

        system_prompt_tab.children = [
            widgets.HTML('<div class="section-header">System Prompt</div>'),
            system_prompt,
            widgets.HTML('<div class="key-status">Customize the system prompt that defines the assistant\'s behavior.</div>')
        ]

        # Quick Edit Profiles Section

        # Profile selection buttons container
        profile_buttons_container = widgets.HBox(
            layout=widgets.Layout(flex_wrap='wrap', margin='10px 0')
        )

        # Create a button for each profile
        for profile_id, profile in profiles.items():
            btn = widgets.Button(
                description=profile['name'],
                layout=widgets.Layout(margin='2px'),
                button_style='info' if profile_id == active_profile else ''
            )
            btn._profile_id = profile_id  # Store profile ID
            profile_buttons[profile_id] = btn
            btn.on_click(on_profile_button_clicked)

        profile_buttons_container.children = list(profile_buttons.values())

        # Profile management buttons
        add_profile_button = widgets.Button(
            description='Add Profile',
            icon='plus',
            button_style='success',
            layout=widgets.Layout(margin='5px')
        )

        delete_profile_button = widgets.Button(
            description='Delete Profile',
            icon='trash',
            button_style='danger',
            layout=widgets.Layout(margin='5px')
        )

        # Profile editing widgets
        profile_name_input = widgets.Text(
            description='Profile Name:',
            layout=widgets.Layout(width='50%')
        )

        # Provider Dropdown for profiles
        profile_provider_dropdown = widgets.Dropdown(
            options=provider_options,
            description='Provider:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='50%')
        )

        profile_model_dropdown = widgets.Dropdown(
            description='Model:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='50%')
        )

        # Load the active profile's provider and model
        profile_data = profiles[active_profile]
        profile_provider = profile_data.get('provider', 'anthropic')  # Default to 'anthropic' if not set
        profile_model = profile_data['model']

        # Ensure the provider is valid
        if profile_provider not in provider_options:
            profile_provider = provider_options[0]

        profile_provider_dropdown.value = profile_provider

        # Update models based on provider
        update_profile_model_options()

        # Ensure the model is valid
        if profile_model in profile_model_dropdown.options:
            profile_model_dropdown.value = profile_model
        elif profile_model_dropdown.options:
            profile_model_dropdown.value = profile_model_dropdown.options[0]
        else:
            profile_model_dropdown.value = None

        # Observe changes in provider dropdown to update models
        profile_provider_dropdown.observe(update_profile_model_options, names='value')

        profile_system_prompt = widgets.Textarea(
            value=profile_data['system_prompt'],
            placeholder='Enter Quick Edit system prompt...',
            description='System Prompt:',
            disabled=False,
            layout=widgets.Layout(width='95%', height='200px')
        )

        # Assemble Quick Edit tab
        quick_edit_tab.children = [
            widgets.HTML('<div class="section-header">Quick Edit Profiles</div>'),
            profile_buttons_container,
            widgets.HBox([add_profile_button, delete_profile_button]),
            widgets.HTML('<div class="section-header">Profile Settings</div>'),
            profile_name_input,
            profile_provider_dropdown,
            profile_model_dropdown,
            profile_system_prompt,
            widgets.HTML('<div class="key-status">Configure how the AI processes your selected text when using Ctrl+Shift+A.</div>')
        ]

        # Custom Providers Section

        # Provider selection dropdown
        provider_options = [(p['name'], name) for name, p in custom_providers.items()]
        if not provider_options:
            provider_options = [("No providers available", None)]
        custom_provider_dropdown = widgets.Dropdown(
            options=provider_options,
            description='Select Provider:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='50%')
        )

        # Input fields for custom provider
        provider_name_input = widgets.Text(
            description='Provider Name:',
            layout=widgets.Layout(width='50%')
        )
        display_name_input = widgets.Text(
            description='Display Name:',
            layout=widgets.Layout(width='50%')
        )
        models_input = widgets.Textarea(
            description='Models (comma-separated):',
            layout=widgets.Layout(width='95%', height='100px')
        )
        initialization_code_input = widgets.Textarea(
            description='Initialization Code:',
            layout=widgets.Layout(width='95%', height='300px')
        )

        # Provider management buttons
        add_new_provider_button = widgets.Button(
            description='Add New',
            button_style='primary',
            icon='plus',
            layout=widgets.Layout(margin='5px')
        )
        delete_provider_button = widgets.Button(
            description='Delete',
            button_style='danger',
            icon='trash',
            layout=widgets.Layout(margin='5px')
        )
        save_provider_button = widgets.Button(
            description='Save',
            button_style='success',
            icon='save',
            layout=widgets.Layout(margin='5px')
        )

        provider_buttons = widgets.HBox([
            add_new_provider_button,
            delete_provider_button,
            save_provider_button
        ])

        # Assemble Custom Providers tab
        custom_providers_tab.children = [
            widgets.HTML('<div class="section-header">Custom Providers</div>'),
            custom_provider_dropdown,
            provider_buttons,
            provider_name_input,
            display_name_input,
            models_input,
            initialization_code_input,
            widgets.HTML('<div class="key-status">Define custom providers with their models and initialization code.</div>')
        ]

        # Update tab children and titles
        tab.children = [api_keys_tab, model_tab, system_prompt_tab, quick_edit_tab, custom_providers_tab]
        tab.set_title(0, "API Keys")
        tab.set_title(1, "Model")
        tab.set_title(2, "System Prompt")
        tab.set_title(3, "Quick Edit")
        tab.set_title(4, "Custom Providers")

        # Create the main container with all widgets
        main_container.children = [
            tab,
            skip_setup_checkbox,
            status_output,
            widgets.HBox([save_button, reset_prompts_button])
        ]

        # Add the main container to the accordion
        accordion.children = [main_container]
        accordion.set_title(0, '🔧 Jupyter Whisper Setup')
        accordion.selected_index = 0  # Open by default

        # Display the accordion (which contains all other widgets)
        display(accordion)

        # Bind button events
        add_profile_button.on_click(on_add_profile_clicked)
        delete_profile_button.on_click(on_delete_profile_clicked)
        save_button.on_click(on_save_clicked)
        reset_prompts_button.on_click(on_reset_prompts_clicked)

        # Bind events for custom providers
        custom_provider_dropdown.observe(on_custom_provider_selected, names='value')
        add_new_provider_button.on_click(on_add_new_provider_clicked)
        delete_provider_button.on_click(on_delete_provider_clicked)
        save_provider_button.on_click(on_save_provider_clicked)

        # Initial button setup
        update_profile_buttons()

    except ImportError:
        print("Please install ipywidgets: pip install ipywidgets")
    except Exception as e:
        print(f"\nError during setup: {str(e)}")
        print("Please try again or report this issue if it persists.")


# Call setup on import if needed
setup_jupyter_whisper()

def initialize_chat():
    """Initialize chat based on configured provider"""
    global c
    config_manager = get_config_manager()
    model, provider = config_manager.get_model()
    system_prompt = config_manager.get_system_prompt()

    try:
        # Get custom providers
        custom_providers = config_manager.get_custom_providers()
        
        # Check if current provider is custom
        if provider in custom_providers:
            c = config_manager.execute_provider_initialization(
                provider_name=provider,
                model=model,
                system_prompt=system_prompt
            )
            globals()['Chat'] = c.__class__
        else:
            # Handle built-in providers
            if provider == "anthropic":
                from claudette import Chat
            elif provider == "openai":
                from cosette import Chat
            elif provider == "xai":
                raise NotImplementedError("XAI provider not yet implemented")
            elif provider == "llama":
                raise NotImplementedError("Llama provider not yet implemented")
            else:
                raise ValueError(f"Unknown provider: {provider}")
            
            globals()['Chat'] = Chat
            c = Chat(model, sp=system_prompt)

        # Update the user namespace
        ip = get_ipython()
        ip.user_ns['c'] = c
        ip.user_ns['Chat'] = globals()['Chat']
        
        return c

    except Exception as e:
        print(f"Error initializing chat: {str(e)}")
        return None

# Initialize global variable
c = None

# Initialize chat when module is loaded
c = initialize_chat()