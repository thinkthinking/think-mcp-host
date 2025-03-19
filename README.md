# Think MCP Host (AI·Zen·Love)

[![Version](https://img.shields.io/badge/version-0.7.5-blue.svg)](https://github.com/thinkthinking/think-mcp-host)

Think MCP Host (AI·Zen·Love) is a Model Context Protocol (MCP) based intelligent agent application that supports various types of large language models, including standard conversational models (LLM), vision language models (VLM), and reasoning models.

![Terminal Interface](https://github.com/user-attachments/assets/fd2debcb-0255-4075-a8aa-11aab5595a4c)

![Chat Interface](https://github.com/user-attachments/assets/d9c2514f-2c97-43b9-a4c3-67786d35977a)

## Features

- Complete MCP (Model Context Protocol) Implementation
  - Full MCP architecture support (Host/Client/Server)
  - Comprehensive MCP resource types support
    - Resources: Dynamic integration of external content
    - Prompts: Template-based system prompts
    - Tools: AI-powered function calls
  - Dynamic MCP command insertion anywhere in conversations
    - Seamless integration of resources into context
    - On-demand prompt template usage
    - Direct tool execution within chat
  - Standalone MCP tool execution support

- Extensive Model Support
  - LLM (Language Models)
    - Text conversations and content generation
    - Programming and code assistance
    - Document writing and analysis
  - VLM (Vision Language Models)
    - Image understanding and analysis
    - Visual content processing
  - Reasoning Models
    - Complex logical analysis
    - Professional domain reasoning
  - Multiple provider support (DeepSeek, OpenAI, OpenRouter, etc.)

- Advanced Conversation Management
  - Automatic conversation history saving
  - Manual save options with countdown timer
  - Historical conversation loading
  - Multiple export format support

- System Features
  - Rich Terminal Interface
    - Beautiful markdown rendering in terminal
    - Syntax highlighting for code blocks
    - Unicode and emoji support
    - Interactive command suggestions
  - Cross-Platform Support
    - Full functionality on Windows, macOS, and Ubuntu
    - Native installation support for each platform
    - Consistent user experience across systems
  - Command-line interface
  - Debug mode support
  - Flexible exit options with save/discard choices

## Usage Guide

### Running Mode Selection

The program supports two main running modes:

1. **Chat Mode** (Default)
   - Used for natural language dialogue
   - Supports multiple LLM models
   - Can use MCP enhancement features

2. **Tool Mode**
   - Used for using specific AI tools
   - Directly calls functions provided by MCP server

### Detailed Usage Process

1. **Select Running Mode**

![alt text](https://github.com/user-attachments/assets/5c204924-33da-4e9c-894a-52aa44e4587c)

- After program startup, you will be prompted to select running mode
- Enter `1` to select Chat mode
- Enter `2` to select Tool mode

2. **Chat Mode Setup Process**
   1. **Select LLM Model**
   ![alt text](https://github.com/user-attachments/assets/5698732b-537b-4a7d-b294-63bd225a1c19)
      - System will display available model list
      - Enter corresponding number to select model
      - Supported models include DeepSeek, Silicon Flow, Volcano Engine, etc.

   2. **Choose Start Method**
   ![alt text](https://github.com/user-attachments/assets/41e99e46-d98b-43ce-be00-fc18e7dc41e8)
      - Option 1: Set system prompt, then start new conversation
      - Option 2: Directly start new conversation (default)
      - Option 3: Load historical conversation

   3. **System Prompt Setting** (if Option 1 was selected)
   ![alt text](https://github.com/user-attachments/assets/405a2676-99b5-49c8-afa9-2563aa3a785e)
      - Can input custom system prompt
      - Supports using `->mcp` command to insert MCP resources

   4. **Load Historical Conversation** (if Option 3 was selected)
   ![alt text](https://github.com/user-attachments/assets/ced64efb-bc9f-470c-b884-fc2d24adae9e)
      - System will display available historical conversation list
      - Select conversation record to load

3. **Tool Mode Setup Process**
   1. **Select MCP Client**
   ![alt text](https://github.com/user-attachments/assets/e64aad0e-d08a-4a27-9109-7f36a4f2d215)
      - System will display available MCP client list
      - Select client to use

   2. **Select Tool**
   ![alt text](https://github.com/user-attachments/assets/8aa663cd-7148-4953-971d-ed7aca50f528)
      - Displays tool list provided by selected client
      - Select specific tool to use

   3. **Execute Tool**
   ![alt text](https://github.com/user-attachments/assets/21c40267-335a-43ae-be88-80e194d1b51d)
   ![alt text](https://github.com/user-attachments/assets/60029ee6-c11e-4195-a1c2-1e08ac2f4543)
      - Provide necessary parameters according to tool requirements
      - View tool execution results

   4. **Continue or Exit**
      - Choose whether to continue using other tools
      - Can switch back to Chat mode at any time

### Basic Chat Mode

1. **Start Conversation**
   - Directly input text to converse
   - Use `Ctrl+C` to exit program

### MCP Enhanced Mode

During conversation, you can use the `->mcp` command to use MCP's enhancement features. Steps are as follows:

1. **Activate MCP Command**
   - Input `->mcp` alone and press Enter in conversation
   - System will guide you through subsequent selections

2. **Select MCP Client**
   ![alt text](https://github.com/user-attachments/assets/e64aad0e-d08a-4a27-9109-7f36a4f2d215)
   - System will display available MCP client list
   - Select client to use

3. **Select MCP Feature Type**
   ![alt text](https://github.com/user-attachments/assets/a2bb43cc-92cb-46cc-a4ac-4e88798199f7)
   System will prompt you to select one of three types:
   1. **Resources**
   ![alt text](https://github.com/user-attachments/assets/c8d60e41-33fb-49ed-ae30-0a042b237931)
      - Input `1` to select
      - Used for selecting and referencing external resources (like images, documents, etc.)
      - Returns format: `->mcp_resources[client_name]:resourceURI`

   2. **Prompts**
    ![alt text](https://github.com/user-attachments/assets/2de4af55-5e17-4a25-92e5-5b72a97b9d29)
      - Input `2` to select
      - Used for selecting predefined prompt templates
      - Returns format: `->mcp_prompts[client_name]:prompt_name{parameters}`

   3. **Tools**
    ![alt text](image-7.png)
      - Input `3` to select
      - Used for selecting and using specific AI tools
      - Returns format: `->mcp_tools[client_name]:tool_name{parameters}`

4. **Complete Selection**
   ![alt text](https://github.com/user-attachments/assets/4b2cb06a-537b-478d-b79f-9aa445d4443c)
   - After selection is complete, system will insert corresponding MCP command in conversation
   - You can continue editing message, or send directly

1. **Select Running Mode**

![alt text](https://github.com/user-attachments/assets/5c204924-33da-4e9c-894a-52aa44e4587c)

- After program startup, you will be prompted to select running mode
- Enter `1` to select Chat mode
- Enter `2` to select Tool mode

2. **Chat Mode Setup Process**
   1. **Select LLM Model**
   ![alt text](https://github.com/user-attachments/assets/5698732b-537b-4a7d-b294-63bd225a1c19)
      - System will display available model list
      - Enter corresponding number to select model
      - Supported models include DeepSeek, Silicon Flow, Volcano Engine, etc.

   2. **Choose Start Method**
   ![alt text](https://github.com/user-attachments/assets/41e99e46-d98b-43ce-be00-fc18e7dc41e8)
      - Option 1: Set system prompt, then start new conversation
      - Option 2: Directly start new conversation (default)
      - Option 3: Load historical conversation

   3. **System Prompt Setting** (if Option 1 was selected)
   ![alt text](https://github.com/user-attachments/assets/405a2676-99b5-49c8-afa9-2563aa3a785e)
      - Can input custom system prompt
      - Supports using `->mcp` command to insert MCP resources

   4. **Load Historical Conversation** (if Option 3 was selected)
   ![alt text](https://github.com/user-attachments/assets/ced64efb-bc9f-470c-b884-fc2d24adae9e)
      - System will display available historical conversation list
      - Select conversation record to load

3. **Tool Mode Setup Process**
   1. **Select MCP Client**
   ![alt text](https://github.com/user-attachments/assets/e64aad0e-d08a-4a27-9109-7f36a4f2d215)
      - System will display available MCP client list
      - Select client to use

   2. **Select Tool**
   ![alt text](https://github.com/user-attachments/assets/8aa663cd-7148-4953-971d-ed7aca50f528)
      - Displays tool list provided by selected client
      - Select specific tool to use

   3. **Execute Tool**
   ![alt text](https://github.com/user-attachments/assets/21c40267-335a-43ae-be88-80e194d1b51d)
   ![alt text](https://github.com/user-attachments/assets/60029ee6-c11e-4195-a1c2-1e08ac2f4543)
      - Provide necessary parameters according to tool requirements
      - View tool execution results

   4. **Continue or Exit**
      - Choose whether to continue using other tools
      - Can switch back to Chat mode at any time

### Basic Chat Mode

1. **Start Conversation**
   - Directly input text to converse
   - Use `Ctrl+C` to exit program

### MCP Enhanced Mode

During conversation, you can use the `->mcp` command to use MCP's enhancement features. Steps are as follows:

1. **Activate MCP Command**
   - Input `->mcp` alone and press Enter in conversation
   - System will guide you through subsequent selections

2. **Select MCP Client**
   ![alt text](https://github.com/user-attachments/assets/e64aad0e-d08a-4a27-9109-7f36a4f2d215)
   - System will display available MCP client list
   - Select client to use

3. **Select MCP Feature Type**
   ![alt text](https://github.com/user-attachments/assets/a2bb43cc-92cb-46cc-a4ac-4e88798199f7)
   System will prompt you to select one of three types:
   1. **Resources**
   ![alt text](https://github.com/user-attachments/assets/c8d60e41-33fb-49ed-ae30-0a042b237931)
      - Input `1` to select
      - Used for selecting and referencing external resources (like images, documents, etc.)
      - Returns format: `->mcp_resources[client_name]:resourceURI`

   2. **Prompts**
    ![alt text](https://github.com/user-attachments/assets/2de4af55-5e17-4a25-92e5-5b72a97b9d29)
      - Input `2` to select
      - Used for selecting predefined prompt templates
      - Returns format: `->mcp_prompts[client_name]:prompt_name{parameters}`

   3. **Tools**
    ![alt text](https://github.com/user-attachments/assets/21c40267-335a-43ae-be88-80e194d1b51d)
      - Input `3` to select
      - Used for selecting and using specific AI tools
      - Returns format: `->mcp_tools[client_name]:tool_name{parameters}`

4. **Complete Selection**
   ![alt text](https://github.com/user-attachments/assets/4b2cb06a-537b-478d-b79f-9aa445d4443c)
   - After selection is complete, system will insert corresponding MCP command in conversation
   - You can continue editing message, or send directly

## Installation and Running

### Development Installation

Before installing from package repositories, you can install the project directly from source for development:

```bash
# Clone the repository
git clone https://github.com/thinkthinking/think-mcp-host.git
cd think-mcp-host

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\Activate.ps1  # On Windows with PowerShell

# Install in development mode with pip
pip install -e .
# or with uv (recommended)
uv pip install -e .
```

### Windows

1. Installation methods
   - Download and double-click `AI-Zen-Love.exe`
   - Or install and run via command line:

```powershell
# Install uv using pip
python -m pip install uv

# Clone the project and install
git clone https://github.com/thinkthinking/think-mcp-host.git
cd think-mcp-host
python -m venv .venv
.venv\Scripts\Activate.ps1
uv pip install -e .
```

2. Configuration file locations
   - LLM configuration: `C:\Users\your-username\.think-llm-client\config\servers_config.json`
   - MCP configuration: `C:\Users\your-username\.think-mcp-client\config\mcp_config.json`
   - History records: `C:\Users\your-username\.think-mcp-host\command_history\`

### macOS

1. Installation methods
   - Download and double-click `AI-Zen-Love.app`
   - Or install and run via terminal:

```bash
# Install uv
python3 -m pip install uv

# Clone the project and install
git clone https://github.com/thinkthinking/think-mcp-host.git
cd think-mcp-host
python3 -m venv .venv
source .venv/bin/activate
uv pip install -e .
```

2. Configuration file locations
   - LLM configuration: `/Users/your-username/.think-llm-client/config/servers_config.json`
   - MCP configuration: `/Users/your-username/.think-mcp-client/config/mcp_config.json`
   - History records: `/Users/your-username/.think-mcp-host/command_history/`

## Configuration Details

### Model Configuration

The project supports three types of models:

1. **LLM (Language Models)**
   - Used for: Text conversations, code writing, document generation
   - Examples: DeepSeek Chat, GPT-4

2. **VLM (Vision Language Models)**
   - Used for: Image understanding and analysis
   - Examples: GPT-4-Vision, Qwen-VL-Plus

3. **Reasoning Models**
   - Used for: Complex reasoning and professional analysis
   - Examples: DeepSeek Reasoner, DeepSeek-R1

### LLM Configuration

The configuration file uses JSON format and needs to be configured according to different model types:

```json
{
  "llm": {
    "providers": {
      "deepseek": {
        "api_key": "<DEEPSEEK_API_KEY>",
        "api_url": "https://api.deepseek.com",
        "model": {
          "deepseek-chat": {
            "max_completion_tokens": 8192
          }
        }
      }
    }
  },
  "vlm": {
    "providers": {
      "openai": {
        "api_key": "<OPENAI_API_KEY>",
        "api_url": "https://api.openai.com/v1",
        "model": {
          "gpt-4-vision": {
            "max_completion_tokens": 4096
          }
        }
      }
    }
  },
  "reasoning": {
    "providers": {
      "deepseek": {
        "api_key": "<DEEPSEEK_API_KEY>",
        "api_url": "https://api.deepseek.com",
        "model": {
          "deepseek-reasoner": {
            "max_completion_tokens": 8192,
            "temperature": 0.6
          }
        }
      }
    }
  }
}
```

Configuration explanation:

1. Choose the configuration area according to model type (llm/vlm/reasoning)
2. Multiple providers can be configured under each type
Configuration instructions for different providers are as follows:

- DeepSeek Documentation: <https://api-docs.deepseek.com/en/>
- Silicon Flow Documentation: <https://docs.siliconflow.cn/en/userguide/quickstart#4-siliconcloud-api-genai>
- Volcano Engine Documentation: <https://www.volcengine.com/docs/82379/1399008>

3. Each provider needs to configure:
   - `api_key`: API key
   - `api_url`: API server address
   - `model`: Specific model configuration
     - `max_completion_tokens`: Maximum output length
     - `temperature`: Temperature parameter (optional)

### MCP Server Configuration

MCP (Model Context Protocol) server configuration example:

```json
{
  "mcpServers": {
    "think-mcp": {
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "--directory",
        "/Users/thinkthinking/src_code/nas/think-mcp",
        "run",
        "think-mcp"
      ]
    }
  }
}
```

### MCP Commands

The following MCP command formats can be used in conversations:

1. Interactive Selection

```bash
 ->mcp 
```

This will start an interactive selection interface, guiding you to choose:

- MCP client
- Operation type (Resources/Prompts/Tools)
- Specific resource/prompt/tool
- Related parameters (if needed)

2. Direct Usage

```bash
# Use resources
->mcp_resources[client_name]:resource_uri

# Use prompts
->mcp_prompts[client_name]:prompt_name{param1:value1,param2:value2}

# Use tools
->mcp_tools[client_name]:tool_name{param1:value1,param2:value2}
```

Examples:

```bash
# Use prompts
->mcp_prompts[think-mcp]:agent-introduction{agent_name:AI Assistant,agent_description:A friendly AI assistant}

# Use tools
->mcp_tools[think-mcp]:analyze_content{text:This is a test text}
```

### Features

- Support for multiple MCP commands in the same input
- Commands can be edited and modified at any time
- Parameters support flexible key-value pair format
- Friendly error prompts

```
### MCP Commands

The following MCP command formats can be used in conversations:

1. Interactive Selection

```bash
 ->mcp 
```

This will start an interactive selection interface, guiding you to choose:

- MCP client
- Operation type (Resources/Prompts/Tools)
- Specific resource/prompt/tool
- Related parameters (if needed)

2. Direct Usage

```bash
# Use resources
->mcp_resources[client_name]:resource_uri

# Use prompts
->mcp_prompts[client_name]:prompt_name{param1:value1,param2:value2}

# Use tools
->mcp_tools[client_name]:tool_name{param1:value1,param2:value2}
```

Examples:

```bash
# Use prompts
->mcp_prompts[think-mcp]:agent-introduction{agent_name:AI Assistant,agent_description:A friendly AI assistant}

# Use tools
->mcp_tools[think-mcp]:analyze_content{text:This is a test text}
```

### Features

- Support for multiple MCP commands in the same input
- Commands can be edited and modified at any time
- Parameters support flexible key-value pair format
- Friendly error prompts

## Releasing New Versions

To release a new version, follow these steps:

1. Update the version number:
   - Update the `version` field in `pyproject.toml`
   - Follow Semantic Versioning

2. Commit changes:

```bash
git add pyproject.toml
git commit -m "chore: bump version to x.x.x"
```

3. Create version tag:

```bash
git tag vx.x.x
git push origin vx.x.x
```
