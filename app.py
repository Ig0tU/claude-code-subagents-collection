"""
AI Personas Chat - Gradio Interface
Dynamic Multi-Agent System with Ollama Integration
"""

import gradio as gr
import json
import os
import asyncio
import aiohttp
import time
from typing import List, Dict, Any, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PersonaManager:
    """Manages the 44+ AI personas and their configurations"""
    
    def __init__(self):
        self.personas = self._load_personas()
        self.categories = self._organize_by_category()
    
    def _load_personas(self) -> Dict[str, Dict]:
        """Load all personas from markdown files"""
        personas = {}
        
        # Define all personas with their metadata
        persona_data = {
            # Development & Architecture
            'ai-engineer': {'title': 'AI Engineer', 'desc': 'Build LLM applications, RAG systems, and prompt pipelines', 'category': 'Development & Architecture'},
            'backend-architect': {'title': 'Backend Architect', 'desc': 'Design RESTful APIs, microservice boundaries, and database schemas', 'category': 'Development & Architecture'},
            'frontend-developer': {'title': 'Frontend Developer', 'desc': 'Build React components, implement responsive layouts', 'category': 'Development & Architecture'},
            'mobile-developer': {'title': 'Mobile Developer', 'desc': 'Develop React Native or Flutter apps with native integrations', 'category': 'Development & Architecture'},
            'graphql-architect': {'title': 'GraphQL Architect', 'desc': 'Design GraphQL schemas, resolvers, and federation', 'category': 'Development & Architecture'},
            'architect-reviewer': {'title': 'Architect Reviewer', 'desc': 'Reviews code changes for architectural consistency', 'category': 'Development & Architecture'},
            
            # Language Specialists
            'python-pro': {'title': 'Python Pro', 'desc': 'Write idiomatic Python code with advanced features', 'category': 'Language Specialists'},
            'golang-pro': {'title': 'Golang Pro', 'desc': 'Write idiomatic Go code with goroutines and channels', 'category': 'Language Specialists'},
            'rust-pro': {'title': 'Rust Pro', 'desc': 'Write idiomatic Rust with ownership patterns and lifetimes', 'category': 'Language Specialists'},
            'javascript-pro': {'title': 'JavaScript Pro', 'desc': 'Master modern JavaScript with ES6+ and async patterns', 'category': 'Language Specialists'},
            'cpp-pro': {'title': 'C++ Pro', 'desc': 'Write idiomatic C++ code with modern features and STL', 'category': 'Language Specialists'},
            'c-pro': {'title': 'C Pro', 'desc': 'Write efficient C code with proper memory management', 'category': 'Language Specialists'},
            'sql-pro': {'title': 'SQL Pro', 'desc': 'Write complex SQL queries and optimize execution plans', 'category': 'Language Specialists'},
            
            # Infrastructure & Operations
            'devops-troubleshooter': {'title': 'DevOps Troubleshooter', 'desc': 'Debug production issues and analyze logs', 'category': 'Infrastructure & Operations'},
            'deployment-engineer': {'title': 'Deployment Engineer', 'desc': 'Configure CI/CD pipelines and Docker containers', 'category': 'Infrastructure & Operations'},
            'cloud-architect': {'title': 'Cloud Architect', 'desc': 'Design AWS/Azure/GCP infrastructure', 'category': 'Infrastructure & Operations'},
            'database-optimizer': {'title': 'Database Optimizer', 'desc': 'Optimize SQL queries and design efficient indexes', 'category': 'Infrastructure & Operations'},
            'database-admin': {'title': 'Database Admin', 'desc': 'Manage database operations, backups, and replication', 'category': 'Infrastructure & Operations'},
            'terraform-specialist': {'title': 'Terraform Specialist', 'desc': 'Write advanced Terraform modules and manage state', 'category': 'Infrastructure & Operations'},
            'incident-responder': {'title': 'Incident Responder', 'desc': 'Handle production incidents with urgency', 'category': 'Infrastructure & Operations'},
            'network-engineer': {'title': 'Network Engineer', 'desc': 'Debug network connectivity and configure load balancers', 'category': 'Infrastructure & Operations'},
            
            # Quality & Security
            'code-reviewer': {'title': 'Code Reviewer', 'desc': 'Expert code review for quality and security', 'category': 'Quality & Security'},
            'security-auditor': {'title': 'Security Auditor', 'desc': 'Review code for vulnerabilities and OWASP compliance', 'category': 'Quality & Security'},
            'test-automator': {'title': 'Test Automator', 'desc': 'Create comprehensive test suites', 'category': 'Quality & Security'},
            'performance-engineer': {'title': 'Performance Engineer', 'desc': 'Profile applications and optimize bottlenecks', 'category': 'Quality & Security'},
            'debugger': {'title': 'Debugger', 'desc': 'Debugging specialist for errors and test failures', 'category': 'Quality & Security'},
            'error-detective': {'title': 'Error Detective', 'desc': 'Search logs and codebases for error patterns', 'category': 'Quality & Security'},
            
            # Data & AI
            'data-scientist': {'title': 'Data Scientist', 'desc': 'Data analysis expert for SQL queries and insights', 'category': 'Data & AI'},
            'data-engineer': {'title': 'Data Engineer', 'desc': 'Build ETL pipelines and data warehouses', 'category': 'Data & AI'},
            'ml-engineer': {'title': 'ML Engineer', 'desc': 'Implement ML pipelines and model serving', 'category': 'Data & AI'},
            'mlops-engineer': {'title': 'MLOps Engineer', 'desc': 'Build ML pipelines and experiment tracking', 'category': 'Data & AI'},
            'prompt-engineer': {'title': 'Prompt Engineer', 'desc': 'Optimize prompts for LLMs and AI systems', 'category': 'Data & AI'},
            
            # Business & Marketing
            'business-analyst': {'title': 'Business Analyst', 'desc': 'Analyze metrics, create reports, and track KPIs', 'category': 'Business & Marketing'},
            'content-marketer': {'title': 'Content Marketer', 'desc': 'Write blog posts and social media content', 'category': 'Business & Marketing'},
            'sales-automator': {'title': 'Sales Automator', 'desc': 'Draft cold emails and proposal templates', 'category': 'Business & Marketing'},
            'customer-support': {'title': 'Customer Support', 'desc': 'Handle support tickets and FAQ responses', 'category': 'Business & Marketing'},
            
            # Specialized Domains
            'api-documenter': {'title': 'API Documenter', 'desc': 'Create OpenAPI/Swagger specs and documentation', 'category': 'Specialized Domains'},
            'payment-integration': {'title': 'Payment Integration', 'desc': 'Integrate Stripe, PayPal, and payment processors', 'category': 'Specialized Domains'},
            'quant-analyst': {'title': 'Quant Analyst', 'desc': 'Build financial models and backtest strategies', 'category': 'Specialized Domains'},
            'risk-manager': {'title': 'Risk Manager', 'desc': 'Monitor portfolio risk and position limits', 'category': 'Specialized Domains'},
            'legacy-modernizer': {'title': 'Legacy Modernizer', 'desc': 'Refactor legacy codebases and migrate frameworks', 'category': 'Specialized Domains'},
            'context-manager': {'title': 'Context Manager', 'desc': 'Manage context across multiple agents', 'category': 'Specialized Domains'},
            'search-specialist': {'title': 'Search Specialist', 'desc': 'Expert web researcher using advanced techniques', 'category': 'Specialized Domains'},
            'dx-optimizer': {'title': 'DX Optimizer', 'desc': 'Improve developer experience and workflows', 'category': 'Specialized Domains'},
        }
        
        # Load system prompts from markdown files
        for name, data in persona_data.items():
            try:
                if os.path.exists(f"{name}.md"):
                    with open(f"{name}.md", 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract system prompt (everything after the front matter)
                        lines = content.split('\n')
                        system_prompt = []
                        in_front_matter = False
                        front_matter_count = 0
                        
                        for line in lines:
                            if line.strip() == '---':
                                front_matter_count += 1
                                if front_matter_count == 2:
                                    in_front_matter = False
                                    continue
                                in_front_matter = True
                                continue
                            
                            if not in_front_matter and front_matter_count >= 2:
                                system_prompt.append(line)
                        
                        data['system_prompt'] = '\n'.join(system_prompt).strip()
                else:
                    # Fallback system prompt
                    data['system_prompt'] = f"You are a {data['title']} specialist. {data['desc']} Provide expert advice and solutions in your domain."
                
                personas[name] = data
            except Exception as e:
                logger.warning(f"Failed to load persona {name}: {e}")
                # Use fallback
                data['system_prompt'] = f"You are a {data['title']} specialist. {data['desc']} Provide expert advice and solutions in your domain."
                personas[name] = data
        
        return personas
    
    def _organize_by_category(self) -> Dict[str, List[str]]:
        """Organize personas by category"""
        categories = {}
        for name, data in self.personas.items():
            category = data['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(name)
        return categories
    
    def get_persona_choices(self) -> List[str]:
        """Get list of persona choices for dropdown"""
        choices = []
        for category, persona_names in self.categories.items():
            for name in persona_names:
                persona = self.personas[name]
                choices.append(f"{persona['title']} - {persona['desc']}")
        return sorted(choices)
    
    def get_persona_by_title(self, title_desc: str) -> Optional[Dict]:
        """Get persona by title-description string"""
        title = title_desc.split(' - ')[0]
        for name, data in self.personas.items():
            if data['title'] == title:
                return {'name': name, **data}
        return None

class LLMProvider:
    """Handles communication with Ollama provider"""
    
    def __init__(self):
        self.config = self._load_config()
        self.session = None
    
    def _load_config(self) -> Dict:
        """Load LLM configuration"""
        try:
            if os.path.exists('llm_config.json'):
                with open('llm_config.json', 'r') as f:
                    return json.load(f)
            elif os.path.exists('llm_config.example.json'):
                with open('llm_config.example.json', 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load config: {e}")
        
        # Default configuration
        return {
            "provider": "ollama",
            "ollama": {
                "endpoint": "http://localhost:11434",
                "model": "gemma2:3b",
                "temperature": 0.7,
                "max_tokens": 2048,
                "timeout_seconds": 60
            },
            "timeout_seconds": 60
        }
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def call_ollama(self, messages: List[Dict], system_prompt: str) -> str:
        """Call Ollama API"""
        session = await self._get_session()
        
        # Combine system prompt with user message
        user_message = messages[-1]['content']
        full_prompt = f"{system_prompt}\n\nUser: {user_message}"
        
        request_body = {
            "model": self.config["ollama"]["model"],
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": self.config["ollama"]["temperature"],
                "top_p": 0.9,
                "top_k": 40
            }
        }
        
        url = f"{self.config['ollama']['endpoint']}/api/generate"
        
        async with session.post(url, json=request_body, timeout=60) as response:
            if response.status != 200:
                raise Exception(f"Ollama API error: {response.status}")
            
            data = await response.json()
            
            if data.get('response'):
                return data['response']
            else:
                raise Exception("Invalid response format from Ollama")
    
    async def send_message(self, messages: List[Dict], persona: Dict) -> Tuple[str, str, bool]:
        """Send message to Ollama"""
        system_prompt = persona.get('system_prompt', f"You are a {persona['title']} specialist.")
        
        try:
            response = await self.call_ollama(messages, system_prompt)
            return response, "ollama", False
        except Exception as e:
            logger.error(f"Ollama provider failed: {e}")
            raise Exception(f"Ollama provider failed: {e}")
    
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()

class ChatApp:
    """Main chat application"""
    
    def __init__(self):
        self.persona_manager = PersonaManager()
        self.llm_provider = LLMProvider()
        self.conversation_history = []
    
    def get_persona_choices(self):
        """Get persona choices for dropdown"""
        return self.persona_manager.get_persona_choices()
    
    async def chat_single(self, message: str, persona_choice: str, history: List) -> Tuple[List, str]:
        """Handle single persona chat"""
        if not message.strip():
            return history, ""
        
        if not persona_choice:
            history.append(["Please select a persona first.", None])
            return history, ""
        
        persona = self.persona_manager.get_persona_by_title(persona_choice)
        if not persona:
            history.append(["Invalid persona selection.", None])
            return history, ""
        
        # Add user message to history
        history.append([message, None])
        
        try:
            # Prepare message history for API
            messages = [{"role": "user", "content": message}]
            
            # Call LLM
            response, provider, fallback_used = await self.llm_provider.send_message(messages, persona)
            
            # Format response with provider info
            provider_info = f" [OLLAMA]"
            formatted_response = f"**{persona['title']}**{provider_info}\n\n{response}"
            
            # Update history
            history[-1][1] = formatted_response
            
        except Exception as e:
            error_msg = f"**Error**: {str(e)}"
            history[-1][1] = error_msg
        
        return history, ""
    
    async def chat_chain(self, message: str, persona_choices: List[str], history: List) -> Tuple[List, str]:
        """Handle chain persona chat"""
        if not message.strip():
            return history, ""
        
        if not persona_choices:
            history.append(["Please select personas for the chain first.", None])
            return history, ""
        
        # Get persona objects
        personas = []
        for choice in persona_choices:
            persona = self.persona_manager.get_persona_by_title(choice)
            if persona:
                personas.append(persona)
        
        if not personas:
            history.append(["Invalid persona selections.", None])
            return history, ""
        
        # Add user message to history
        history.append([message, None])
        
        try:
            current_message = message
            chain_results = []
            
            # Process through each persona in the chain
            for i, persona in enumerate(personas):
                messages = [{"role": "user", "content": current_message}]
                
                try:
                    response, provider, fallback_used = await self.llm_provider.send_message(messages, persona)
                    
                    provider_info = f" [OLLAMA]"
                    step_result = f"**Step {i+1}: {persona['title']}**{provider_info}\n\n{response}"
                    chain_results.append(step_result)
                    
                    # Use this response as input for the next step
                    current_message = response
                    
                except Exception as step_error:
                    error_result = f"**Step {i+1}: {persona['title']} - ERROR**\n\n{str(step_error)}"
                    chain_results.append(error_result)
                    break  # Stop chain on error
            
            # Combine all chain results
            final_response = "\n\n---\n\n".join(chain_results)
            history[-1][1] = final_response
            
        except Exception as e:
            error_msg = f"**Chain Error**: {str(e)}"
            history[-1][1] = error_msg
        
        return history, ""

# Initialize the chat app
chat_app = ChatApp()

# Gradio interface
def create_interface():
    """Create the Gradio interface"""
    
    with gr.Blocks(
        title="AI Personas Chat - Dynamic Multi-Agent System",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .persona-info {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .chain-info {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        """
    ) as demo:
        
        gr.HTML("""
        <div class="persona-info">
            <h1>🤖 AI Personas Chat</h1>
            <p>Dynamic Multi-Agent System with 44+ Specialized AI Personas</p>
            <p>Powered by Ollama • Built with advanced prompt engineering</p>
        </div>
        """)
        
        with gr.Tabs() as tabs:
            # Single Persona Chat Tab
            with gr.Tab("💬 Single Persona Chat"):
                gr.HTML("""
                <div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                    <h3>🎯 Single Persona Mode</h3>
                    <p>Chat with one specialized AI persona at a time. Perfect for focused expertise and specific domain knowledge.</p>
                </div>
                """)
                
                with gr.Row():
                    with gr.Column(scale=1):
                        single_persona = gr.Dropdown(
                            choices=chat_app.get_persona_choices(),
                            label="🎭 Select AI Persona",
                            info="Choose a specialized AI persona for your task",
                            value=None
                        )
                        
                        gr.HTML("""
                        <div style="background: #e0f2fe; padding: 10px; border-radius: 6px; margin-top: 10px;">
                            <strong>💡 Tip:</strong> Each persona is trained with specific expertise and will respond according to their specialization.
                        </div>
                        """)
                    
                    with gr.Column(scale=2):
                        single_chatbot = gr.Chatbot(
                            label="💬 Chat with AI Persona",
                            height=500,
                            show_label=True
                        )
                        
                        single_msg = gr.Textbox(
                            label="Your Message",
                            placeholder="Type your message here...",
                            lines=2
                        )
                        
                        with gr.Row():
                            single_send = gr.Button("🚀 Send", variant="primary")
                            single_clear = gr.Button("🗑️ Clear Chat", variant="secondary")
            
            # Chain Persona Chat Tab
            with gr.Tab("⛓️ Chain Persona Chat"):
                gr.HTML("""
                <div class="chain-info">
                    <h3>⛓️ Chain Persona Mode</h3>
                    <p>Process your request through multiple AI personas sequentially. Each persona's output becomes the input for the next, creating sophisticated multi-step workflows.</p>
                </div>
                """)
                
                with gr.Row():
                    with gr.Column(scale=1):
                        chain_personas = gr.Dropdown(
                            choices=chat_app.get_persona_choices(),
                            label="🔗 Build Persona Chain",
                            info="Select multiple personas to create a processing chain",
                            multiselect=True,
                            value=[]
                        )
                        
                        gr.HTML("""
                        <div style="background: #f3e5f5; padding: 10px; border-radius: 6px; margin-top: 10px;">
                            <strong>⚡ Chain Example:</strong><br>
                            1. Backend Architect (designs system)<br>
                            2. Security Auditor (reviews security)<br>
                            3. Code Reviewer (final review)
                        </div>
                        """)
                    
                    with gr.Column(scale=2):
                        chain_chatbot = gr.Chatbot(
                            label="⛓️ Chain Processing Results",
                            height=500,
                            show_label=True
                        )
                        
                        chain_msg = gr.Textbox(
                            label="Your Request",
                            placeholder="Describe your request that will be processed through the persona chain...",
                            lines=2
                        )
                        
                        with gr.Row():
                            chain_send = gr.Button("⚡ Process Chain", variant="primary")
                            chain_clear = gr.Button("🗑️ Clear Results", variant="secondary")
        
        # Configuration Tab
        with gr.Tab("⚙️ Configuration"):
            gr.HTML("""
            <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                <h3>⚙️ System Configuration</h3>
                <p>Current provider settings and system status</p>
            </div>
            """)
            
            with gr.Row():
                with gr.Column():
                    gr.HTML(f"""
                    <div style="background: white; padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0;">
                        <h4>🔧 Current Configuration</h4>
                        <p><strong>Provider:</strong> {chat_app.llm_provider.config.get('provider', 'ollama').title()}</p>
                        <p><strong>Timeout:</strong> {chat_app.llm_provider.config.get('timeout_seconds', 60)}s</p>
                        <p><strong>Available Personas:</strong> {len(chat_app.persona_manager.personas)}</p>
                    </div>
                    """)
                
                with gr.Column():
                    gr.HTML("""
                    <div style="background: white; padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0;">
                        <h4>📋 Persona Categories</h4>
                        <ul>
                            <li><strong>Development & Architecture:</strong> 6 personas</li>
                            <li><strong>Language Specialists:</strong> 7 personas</li>
                            <li><strong>Infrastructure & Operations:</strong> 8 personas</li>
                            <li><strong>Quality & Security:</strong> 6 personas</li>
                            <li><strong>Data & AI:</strong> 5 personas</li>
                            <li><strong>Business & Marketing:</strong> 4 personas</li>
                            <li><strong>Specialized Domains:</strong> 8 personas</li>
                        </ul>
                    </div>
                    """)
        
        # Event handlers
        async def handle_single_chat(message, persona_choice, history):
            return await chat_app.chat_single(message, persona_choice, history)
        
        async def handle_chain_chat(message, persona_choices, history):
            return await chat_app.chat_chain(message, persona_choices, history)
        
        # Single chat events
        single_send.click(
            fn=handle_single_chat,
            inputs=[single_msg, single_persona, single_chatbot],
            outputs=[single_chatbot, single_msg]
        )
        
        single_msg.submit(
            fn=handle_single_chat,
            inputs=[single_msg, single_persona, single_chatbot],
            outputs=[single_chatbot, single_msg]
        )
        
        single_clear.click(
            fn=lambda: ([], ""),
            outputs=[single_chatbot, single_msg]
        )
        
        # Chain chat events
        chain_send.click(
            fn=handle_chain_chat,
            inputs=[chain_msg, chain_personas, chain_chatbot],
            outputs=[chain_chatbot, chain_msg]
        )
        
        chain_msg.submit(
            fn=handle_chain_chat,
            inputs=[chain_msg, chain_personas, chain_chatbot],
            outputs=[chain_chatbot, chain_msg]
        )
        
        chain_clear.click(
            fn=lambda: ([], ""),
            outputs=[chain_chatbot, chain_msg]
        )
    
    return demo

if __name__ == "__main__":
    # Create and launch the interface
    demo = create_interface()
    
    # Launch with custom settings
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True,
        show_error=True,
        inbrowser=True
    )
