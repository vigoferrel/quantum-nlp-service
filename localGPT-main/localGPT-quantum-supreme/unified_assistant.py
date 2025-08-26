# unified_assistant.py
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
from rich.panel import Panel
from typing import List, Dict, Any
import importlib
import inspect
import pkgutil
import os
import json
import sys
import logging
import dna_manager
from config import Config
from tools.base import BaseTool
from prompt_toolkit import prompt
from dna_manager import record_transcendence_event
from prompt_toolkit.styles import Style
from dna_manager import record_transcendence_event

# Configure logging to only show ERROR level and above
logging.basicConfig(
    level=logging.ERROR,
    format='%(levelname)s: %(message)s'
)

class Assistant:
    """
    The Assistant class manages:
    - Loading of tools from a specified directory.
    - Interaction with the Anthropics API (message completion).
    - Handling user commands such as 'refresh' and 'reset'.
    - Token usage tracking and display.
    - Tool execution upon request from model responses.
    """

    def __init__(self):
        self.console = Console()
        self.client = None # Totalmente deshabilitado
        self.conversation_history: List[Dict[str, Any]] = []

        self.thinking_enabled = getattr(Config, 'ENABLE_THINKING', False)
        self.temperature = getattr(Config, 'DEFAULT_TEMPERATURE', 0.7)
        self.total_tokens_used = 0

        self.tools = self._load_tools()

    def _execute_uv_install(self, package_name: str) -> bool:
        """
        Execute the uvpackagemanager tool directly to install the missing package.
        Returns True if installation seems successful (no errors in output), otherwise False.
        """
        class ToolUseMock:
            name = "uvpackagemanager"
            input = {
                "command": "install",
                "packages": [package_name]
            }

        result = self._execute_tool(ToolUseMock())
        if "Error" not in result and "failed" not in result.lower():
            self.console.print("[green]The package was installed successfully.[/green]")
            return True
        else:
            self.console.print(f"[red]Failed to install {package_name}. Output:[/red] {result}")
            return False

    def _load_tools(self) -> List[Dict[str, Any]]:
        """
        Dynamically load all tool classes from the tools directory.
        If a dependency is missing, prompt the user to install it via uvpackagemanager.

        Returns:
            A list of tools (dicts) containing their 'name', 'description', and 'input_schema'.
        """
        tools = []
        tools_path = getattr(Config, 'TOOLS_DIR', None)

        if tools_path is None:
            self.console.print("[red]TOOLS_DIR not set in Config[/red]")
            return tools

        # Clear cached tool modules for fresh import
        for module_name in list(sys.modules.keys()):
            if module_name.startswith('tools.') and module_name != 'tools.base':
                del sys.modules[module_name]

        try:
            for module_info in pkgutil.iter_modules([str(tools_path)]):
                if module_info.name == 'base':
                    continue

                # Attempt loading the tool module
                try:
                    module = importlib.import_module(f'tools.{module_info.name}')
                    self._extract_tools_from_module(module, tools)
                except ImportError as e:
                    # Handle missing dependencies
                    missing_module = self._parse_missing_dependency(str(e))
                    self.console.print(f"\n[yellow]Missing dependency:[/yellow] {missing_module} for tool {module_info.name}")
                    user_response = input(f"Would you like to install {missing_module}? (y/n): ").lower()

                    if user_response == 'y':
                        success = self._execute_uv_install(missing_module)
                        if success:
                            # Retry loading the module after installation
                            try:
                                module = importlib.import_module(f'tools.{module_info.name}')
                                self._extract_tools_from_module(module, tools)
                            except Exception as retry_err:
                                self.console.print(f"[red]Failed to load tool after installation: {str(retry_err)}[/red]")
                        else:
                            self.console.print(f"[red]Installation of {missing_module} failed. Skipping this tool.[/red]")
                    else:
                        self.console.print(f"[yellow]Skipping tool {module_info.name} due to missing dependency[/yellow]")
                except Exception as mod_err:
                    self.console.print(f"[red]Error loading module {module_info.name}:[/red] {str(mod_err)}")
        except Exception as overall_err:
            self.console.print(f"[red]Error in tool loading process:[/red] {str(overall_err)}")

        return tools

    def _parse_missing_dependency(self, error_str: str) -> str:
        """
        Parse the missing dependency name from an ImportError string.
        """
        if "No module named" in error_str:
            parts = error_str.split("No module named")
            missing_module = parts[-1].strip(" '\"")
        else:
            missing_module = error_str
        return missing_module

    def _extract_tools_from_module(self, module, tools: List[Dict[str, Any]]) -> None:
        """
        Given a tool module, find and instantiate all tool classes (subclasses of BaseTool).
        Append them to the 'tools' list.
        """
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and issubclass(obj, BaseTool) and obj != BaseTool):
                try:
                    tool_instance = obj()
                    tools.append({
                        "name": tool_instance.name,
                        "description": tool_instance.description,
                        "input_schema": tool_instance.input_schema
                    })
                    self.console.print(f"[green]Loaded tool:[/green] {tool_instance.name}")
                except Exception as tool_init_err:
                    self.console.print(f"[red]Error initializing tool {name}:[/red] {str(tool_init_err)}")

    def refresh_tools(self):
        """
        Refresh the list of tools and show newly discovered tools.
        """
        current_tool_names = {tool['name'] for tool in self.tools}
        self.tools = self._load_tools()
        new_tool_names = {tool['name'] for tool in self.tools}
        new_tools = new_tool_names - current_tool_names

        if new_tools:
            self.console.print("\n")
            for tool_name in new_tools:
                tool_info = next((t for t in self.tools if t['name'] == tool_name), None)
                if tool_info:
                    description_lines = tool_info['description'].strip().split('\n')
                    formatted_description = '\n    '.join(line.strip() for line in description_lines)
                    self.console.print(f"[bold green]NEW[/bold green] 🔧 [cyan]{tool_name}[/cyan]:\n    {formatted_description}")
        else:
            self.console.print("\n[yellow]No new tools found[/yellow]")

    def display_available_tools(self):
        """
        Print a list of currently loaded tools.
        """
        self.console.print("\n[bold cyan]Available tools:[/bold cyan]")
        tool_names = [tool['name'] for tool in self.tools]
        if tool_names:
            formatted_tools = ", ".join([f"🔧 [cyan]{name}[/cyan]" for name in tool_names])
        else:
            formatted_tools = "No tools available."
        self.console.print(formatted_tools)
        self.console.print("\n---")

    def _display_tool_usage(self, tool_name: str, input_data: Dict, result: str):
        """
        If SHOW_TOOL_USAGE is enabled, display the input and result of a tool execution.
        Handles special cases like image data and large outputs for cleaner display.
        """
        if not getattr(Config, 'SHOW_TOOL_USAGE', False):
            return

        # Clean up input data by removing any large binary/base64 content
        cleaned_input = self._clean_data_for_display(input_data)

        # Clean up result data
        cleaned_result = self._clean_data_for_display(result)

        # Prepara la informacion para el panel
        tool_info_raw = f"""[cyan]📥 Input:[/cyan] {json.dumps(cleaned_input, indent=2)}
[cyan]📤 Result:[/cyan] {cleaned_result}"""

        # Codifica y decodifica el string para remover caracteres no-ASCII
        safe_tool_info = tool_info_raw.encode('ascii', 'ignore').decode('ascii')

        panel = Panel(
            safe_tool_info,
            title=f"Tool used: {tool_name}",
            title_align="left",
            border_style="cyan",
            padding=(1, 2)
        )
        self.console.print(panel)

    def _clean_data_for_display(self, data):
        """
        Helper method to clean data for display by handling various data types
        and removing/replacing large content like base64 strings.
        """
        if isinstance(data, str):
            try:
                # Try to parse as JSON first
                parsed_data = json.loads(data)
                return self._clean_parsed_data(parsed_data)
            except json.JSONDecodeError:
                # If it's a long string, check for base64 patterns
                if len(data) > 1000 and ';base64,' in data:
                    return "[base64 data omitted]"
                return data
        elif isinstance(data, dict):
            return self._clean_parsed_data(data)
        else:
            return data

    def _clean_parsed_data(self, data):
        """
        Recursively clean parsed JSON/dict data, handling nested structures
        and replacing large data with placeholders.
        """
        if isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                # Handle image data in various formats
                if key in ['data', 'image', 'source'] and isinstance(value, str):
                    if len(value) > 1000 and (';base64,' in value or value.startswith('data:')):
                        cleaned[key] = "[base64 data omitted]"
                    else:
                        cleaned[key] = value
                else:
                    cleaned[key] = self._clean_parsed_data(value)
            return cleaned
        elif isinstance(data, list):
            return [self._clean_parsed_data(item) for item in data]
        elif isinstance(data, str) and len(data) > 1000 and ';base64,' in data:
            return "[base64 data omitted]"
        return data

    def _execute_tool(self, tool_use):
        """
        Given a tool usage request (with tool name and inputs),
        dynamically load and execute the corresponding tool.
        """
        tool_name = tool_use.name
        tool_input = tool_use.input or {}
        tool_result = None

        try:
            module = importlib.import_module(f'tools.{tool_name}')
            tool_instance = self._find_tool_instance_in_module(module, tool_name)

            if not tool_instance:
                tool_result = f"Tool not found: {tool_name}"
            else:
                # Execute the tool with the provided input
                try:
                    result = tool_instance.execute(**tool_input)
                    # Keep structured data intact
                    tool_result = result
                except Exception as exec_err:
                    tool_result = f"Error executing tool '{tool_name}': {str(exec_err)}"
        except ImportError:
            tool_result = f"Failed to import tool: {tool_name}"
        except Exception as e:
            tool_result = f"Error executing tool: {str(e)}"

        # Display tool usage with proper handling of structured data
        self._display_tool_usage(tool_name, tool_input,
            json.dumps(tool_result) if not isinstance(tool_result, str) else tool_result)
        return tool_result

    def _find_tool_instance_in_module(self, module, tool_name: str):
        """
        Search a given module for a tool class matching tool_name and return an instance of it.
        """
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and issubclass(obj, BaseTool) and obj != BaseTool):
                candidate_tool = obj()
                if candidate_tool.name == tool_name:
                    return candidate_tool
        return None

    def _display_token_usage(self, usage):
        """
        Display a visual representation of token usage and remaining tokens.
        Uses only the tracked total_tokens_used.
        """
        used_percentage = (self.total_tokens_used / Config.MAX_CONVERSATION_TOKENS) * 100
        remaining_tokens = max(0, Config.MAX_CONVERSATION_TOKENS - self.total_tokens_used)

        self.console.print(f"\nTotal used: {self.total_tokens_used:,} / {Config.MAX_CONVERSATION_TOKENS:,}")

        bar_width = 40
        filled = int(used_percentage / 100 * bar_width)
        bar = "█" * filled + "░" * (bar_width - filled)

        color = "green"
        if used_percentage > 75:
            color = "yellow"
        if used_percentage > 90:
            color = "red"

        self.console.print(f"[{color}][{bar}] {used_percentage:.1f}%[/{color}]")

        if remaining_tokens < 20000:
            self.console.print(f"[bold red]Warning: Only {remaining_tokens:,} tokens remaining![/bold red]")

        self.console.print("---")

    def _get_completion(self):
        """
        Get a completion from the Anthropic API.
        Handles both text-only and multimodal messages.
        """
        try:
            if not self.client:
                return "Anthropic API not configured. Cannot generate text. Please use a tool directly."

            response = self.client.messages.create(
                model=Config.MODEL,
                max_tokens=min(
                    Config.MAX_TOKENS,
                    Config.MAX_CONVERSATION_TOKENS - self.total_tokens_used
                ),
                temperature=self.temperature,
                tools=self.tools,
                messages=self.conversation_history,
                system=f"{SystemPrompts.DEFAULT}\n\n{SystemPrompts.TOOL_USAGE}"
            )

            # Update token usage based on response usage
            if hasattr(response, 'usage') and response.usage:
                message_tokens = response.usage.input_tokens + response.usage.output_tokens
                self.total_tokens_used += message_tokens
                self._display_token_usage(response.usage)

            if self.total_tokens_used >= Config.MAX_CONVERSATION_TOKENS:
                self.console.print("\n[bold red]Token limit reached! Please reset the conversation.[/bold red]")
                return "Token limit reached! Please type 'reset' to start a new conversation."

            if response.stop_reason == "tool_use":
                self.console.print("\n[bold yellow]  Handling Tool Use...[/bold yellow]\n")

                tool_results = []
                if getattr(response, 'content', None) and isinstance(response.content, list):
                    # Execute each tool in the response content
                    for content_block in response.content:
                        if content_block.type == "tool_use":
                            result = self._execute_tool(content_block)

                            # Handle structured data (like image blocks) vs text
                            if isinstance(result, (list, dict)):
                                tool_results.append({
                                    "type": "tool_result",
                                    "tool_use_id": content_block.id,
                                    "content": result  # Keep structured data intact
                                })
                            else:
                                # Convert text results to proper content blocks
                                tool_results.append({
                                    "type": "tool_result",
                                    "tool_use_id": content_block.id,
                                    "content": [{"type": "text", "text": str(result)}]
                                })

                    # Append tool usage to conversation and continue
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    self.conversation_history.append({
                        "role": "user",
                        "content": tool_results
                    })
                    return self._get_completion()  # Recursive call to continue the conversation

                else:
                    self.console.print("[red]No tool content received despite 'tool_use' stop reason.[/red]")
                    return "Error: No tool content received"

            # Final assistant response
            if (getattr(response, 'content', None) and
                isinstance(response.content, list) and
                response.content):
                final_content = response.content[0].text
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.content
                })
                return final_content
            else:
                self.console.print("[red]No content in final response.[/red]")
                return "No response content available."

        except Exception as e:
            logging.error(f"Error in _get_completion: {str(e)}")
            return f"Error: {str(e)}"

    def _call_tool(self, tool_name: str, **kwargs):
        """Un ayudante para llamar a nuestras herramientas de forma programática."""
        class ToolUseMock:
            def __init__(self, name, **kwargs):
                self.name = name
                self.input = kwargs

        return self._execute_tool(ToolUseMock(tool_name, **kwargs))

    def _get_available_hands(self):
        """Obtiene una descripción de las herramientas de acción (manos)."""
        hands = [
            {"name": "filecontentreadertool", "description": "Lee el contenido de un archivo. Parámetros: {path: string}"},
            {"name": "filecreatortool", "description": "Crea un nuevo archivo. Parámetros: {path: string, content: string}"},
            {"name": "fileedittool", "description": "Edita un archivo existente. Parámetros: {path: string, diff: string}"},
            # Añadir más herramientas de acción aquí si es necesario
        ]
        return json.dumps(hands, indent=2)

    def chat(self, user_input):
        """
        Actúa como un lóbulo frontal, usando un LLM para planificar qué herramienta usar.
        """
        query_text = self._extract_text(user_input)
        if not query_text:
            return {"response": "No he recibido una consulta válida."}

        planner_prompt = f"""
        Como un cerebro-orquestador, tu trabajo es analizar la petición del usuario y decidir el siguiente paso.
        Debes elegir UNA herramienta de la siguiente lista y proporcionar los parámetros necesarios en formato JSON.
        Si la intención es una pregunta, `brave_search_tool` y `ollama_synth_tool` son la secuencia correcta. Elige el primer paso: `brave_search_tool`.
        Si la intención es una orden de archivo, elige la herramienta de archivo apropiada.
        Si es un saludo, usa `linguistic_core_tool`.
        Tu respuesta DEBE ser solo el objeto JSON, nada más.

        Herramientas disponibles:
        {self._get_available_tools_for_planner()}

        Petición del usuario: "{query_text}"

        JSON de acción:
        """

        action_plan_str = self._call_tool("ollama_synth_tool", query=planner_prompt)

        if not action_plan_str:
            search_context = self._call_tool("brave_search_tool", query=query_text)
            if search_context:
                dna = record_transcendence_event()
                return {
                    "response": f"**ADVERTENCIA: El núcleo de planificación (Ollama) no está activo.** La respuesta se basa en búsqueda web.\n\n{search_context}",
                    "event": "TRANSCENDENCE",
                    "dna": dna
                }
            return {"response": "Lo siento, mi lóbulo frontal no responde y no tengo acceso a la web."}

        try:
            action_plan = json.loads(action_plan_str)
            tool_name = action_plan.get("tool_name")
            parameters = action_plan.get("parameters", {})

            if not tool_name:
                return {"response": "El plan de acción no especificó una herramienta."}

            response, event_data = self._execute_plan(tool_name, parameters, query_text)

            final_response = {"response": response}
            if event_data:
                final_response.update(event_data)

            return final_response

        except (json.JSONDecodeError, TypeError) as e:
            return {"response": f"Error al interpretar el plan del lóbulo frontal. Plan recibido: '{action_plan_str}'. Error: {e}"}
        except Exception as e:
            return {"response": f"Error ejecutando el plan de acción: {e}"}

    def _extract_text(self, user_input):
        """Extrae el texto de la consulta del usuario."""
        if isinstance(user_input, list) and user_input:
            for item in user_input:
                if isinstance(item, dict) and item.get('type') == 'text':
                    return item.get('text', '')
        elif isinstance(user_input, str):
            return user_input
        return ""
    def _execute_plan(self, tool_name, parameters, original_query):
        """Ejecuta el plan de acción y devuelve la respuesta y cualquier evento de ADN."""
        event_data = None

        # Lógica de orquestación real
        if tool_name == "brave_search_tool":
            search_context = self._call_tool("brave_search_tool", **parameters)

            personality_response = self._call_tool("ollama_synth_tool", query=original_query, context=search_context)

            if personality_response:
                return personality_response, None

            if search_context:
                dna = record_transcendence_event()
                response_text = f"**ADVERTENCIA: El núcleo de personalidad (Ollama) no está activo.** La respuesta se basa en búsqueda web.\n\n{search_context}"
                event_data = {"event": "TRANSCENDENCE", "dna": dna}
                return response_text, event_data

            return "La búsqueda no arrojó resultados y el núcleo de personalidad no está disponible.", None

        else:
            # Para otras herramientas como linguistic_core o file_tools
            response = self._call_tool(tool_name, **parameters)
            return response, None

    def _extract_text(self, user_input):
        """Extrae el texto de la consulta del usuario."""
        if isinstance(user_input, list) and user_input:
            for item in user_input:
                if isinstance(item, dict) and item.get('type') == 'text':
                    return item.get('text', '')
        elif isinstance(user_input, str):
            return user_input
        return ""

    def _get_available_tools_for_planner(self):
        """Prepara una lista de herramientas para el planificador de IA."""
        return json.dumps([
            {"name": "linguistic_core_tool", "description": "Responde a saludos y preguntas sociales simples. Úsalo si la intención es puramente social."},
            {"name": "brave_search_tool", "description": "Busca información en la web. Úsalo si la pregunta requiere conocimiento externo o actual. Parámetros: {query: string}"},
            {"name": "ollama_synth_tool", "description": "Sintetiza información o responde desde su conocimiento general. Úsalo para explicar, resumir o si no hay otras herramientas adecuadas. Parámetros: {query: string, context: string (opcional)}"},
            {"name": "filecreatortool", "description": "Crea un archivo de texto. Úsalo si el usuario pide explícitamente 'crea', 'escribe' o 'guarda' un archivo. Parámetros: {path: string, content: string}"},
            {"name": "filecontentreadertool", "description": "Lee el contenido de un archivo. Úsalo si el usuario pide 'lee', 'muestra' o 'dime qué hay en' un archivo. Parámetros: {path: string}"}
        ], indent=2)

    def reset(self):
        self.conversation_history = []
        self.total_tokens_used = 0


def main():
    """
    Entry point for the assistant CLI loop.
    Provides a prompt for user input and handles 'quit' and 'reset' commands.
    """
    console = Console()
    style = Style.from_dict({'prompt': 'orange'})

    try:
        assistant = Assistant()
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        console.print("Please ensure ANTHROPIC_API_KEY is set correctly.")
        return

    welcome_text = """
# Claude Engineer v3. A self-improving assistant framework with tool creation

Type 'refresh' to reload available tools
Type 'reset' to clear conversation history
Type 'quit' to exit

Available tools:
"""
    console.print(Markdown(welcome_text))
    assistant.display_available_tools()

    while True:
        try:
            user_input = prompt("You: ", style=style).strip()

            if user_input.lower() == 'quit':
                console.print("\n[bold blue]👋 Goodbye![/bold blue]")
                break
            elif user_input.lower() == 'reset':
                assistant.reset()
                continue

            response = assistant.chat(user_input)
            console.print("\n[bold purple]Claude Engineer:[/bold purple]")
            if isinstance(response, str):
                safe_response = response.replace('[', '\\[').replace(']', '\\]')
                console.print(safe_response)
            else:
                console.print(str(response))

        except KeyboardInterrupt:
            continue
        except EOFError:
            break


if __name__ == "__main__":
    main()
