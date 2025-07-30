/**
 * Chat API Integration for Ollama Provider
 * Handles real API calls with dream-like consciousness parameters
 */

class ChatAPI {
    constructor() {
        this.config = null;
        this.currentProvider = 'ollama';
        this.dreamMode = true;
        this.loadConfiguration();
    }

    // Load configuration from JSON file or localStorage
    async loadConfiguration() {
        try {
            // Try to load from llm_config.json first
            const response = await fetch('llm_config.json');
            if (response.ok) {
                this.config = await response.json();
            } else {
                // Fallback to example config
                const exampleResponse = await fetch('llm_config.example.json');
                this.config = await exampleResponse.json();
            }
            
            this.currentProvider = this.config.provider || 'ollama';
            this.dreamMode = this.config.dream_parameters?.consciousness_stream !== false;
            
            console.log('Configuration loaded:', this.config);
        } catch (error) {
            console.error('Failed to load configuration:', error);
            this.useDefaultConfig();
        }
    }

    // Use default configuration with dream-like parameters
    useDefaultConfig() {
        this.config = {
            provider: 'ollama',
            ollama: {
                endpoint: 'http://localhost:11434',
                model: 'gemma2:3b',
                temperature: 0.9,  // Higher creativity for dream-like responses
                max_tokens: 4096,  // More space for elaborate responses
                top_p: 0.95,       // More diverse token selection
                top_k: 50,         // Broader vocabulary choices
                repeat_penalty: 1.2, // Reduce repetition
                dream_mode: true,   // Enable lucid dreaming parameters
                consciousness_level: 'lucid', // Awareness level
                creativity_boost: 1.3,        // Enhanced imagination
                narrative_flow: 'stream',     // Flowing thought patterns
                reality_anchor: 0.3          // Low reality constraint for dreams
            },
            timeout_seconds: 60,
            retry_attempts: 3,
            dream_parameters: {
                lucidity: 0.8,           // How aware the AI is of being in a dream
                vividness: 0.9,          // How detailed and rich responses are
                surrealism: 0.6,         // How much to bend reality
                emotional_depth: 0.8,    // Emotional resonance in responses
                metaphor_density: 0.7,   // Use of metaphorical language
                time_distortion: 0.5,    // Non-linear narrative flow
                consciousness_stream: true // Stream-of-consciousness style
            }
        };
    }

    // Get system prompt for a specific persona
    async getPersonaPrompt(personaName) {
        try {
            const response = await fetch(`${personaName}.md`);
            if (response.ok) {
                const content = await response.text();
                // Extract the system prompt from the markdown file
                const lines = content.split('\n');
                let systemPrompt = '';
                let inSystemSection = false;
                
                for (const line of lines) {
                    if (line.startsWith('---') && systemPrompt) {
                        break; // End of front matter
                    }
                    if (line.startsWith('---')) {
                        continue; // Skip front matter start
                    }
                    if (!line.startsWith('name:') && !line.startsWith('description:')) {
                        systemPrompt += line + '\n';
                    }
                }
                
                return systemPrompt.trim();
            }
        } catch (error) {
            console.error(`Failed to load persona ${personaName}:`, error);
        }
        
        // Fallback system prompt
        return `You are a ${personaName.replace('-', ' ')} specialist. Provide expert advice and solutions in your domain.`;
    }

    // Call Ollama API with dream-like consciousness parameters
    async callOllamaAPI(messages, persona) {
        const systemPrompt = await this.getPersonaPrompt(persona.name);
        const dreamParams = this.config.dream_parameters || {};
        
        // Enhance system prompt with dream-like consciousness
        const enhancedPrompt = this.enhancePromptWithDreamParameters(systemPrompt, persona, dreamParams);
        
        const requestBody = {
            model: this.config.ollama.model || 'gemma2:3b',
            prompt: `${enhancedPrompt}\n\nUser: ${messages[messages.length - 1].content}`,
            stream: false,
            options: {
                temperature: this.config.ollama.temperature || 0.9,
                top_p: this.config.ollama.top_p || 0.95,
                top_k: this.config.ollama.top_k || 50,
                repeat_penalty: this.config.ollama.repeat_penalty || 1.2,
                num_predict: this.config.ollama.max_tokens || 4096,
                // Dream-specific parameters
                mirostat: 2,           // Enable Mirostat sampling for more coherent dreams
                mirostat_tau: 5.0,     // Target entropy for dream-like flow
                mirostat_eta: 0.1,     // Learning rate for adaptive sampling
                tfs_z: 1.0,           // Tail free sampling for creativity
                typical_p: 0.7        // Typical sampling for natural flow
            }
        };

        const response = await fetch(
            `${this.config.ollama.endpoint}/api/generate`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody),
                signal: AbortSignal.timeout((this.config.ollama.timeout_seconds || 60) * 1000)
            }
        );

        if (!response.ok) {
            throw new Error(`Ollama API error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        
        if (data.response) {
            return data.response;
        } else {
            throw new Error('Invalid response format from Ollama API');
        }
    }

    // Enhanced prompt with dream-like consciousness parameters
    enhancePromptWithDreamParameters(systemPrompt, persona, dreamParams) {
        const lucidityLevel = dreamParams.lucidity || 0.8;
        const vividness = dreamParams.vividness || 0.9;
        const surrealism = dreamParams.surrealism || 0.6;
        const emotionalDepth = dreamParams.emotional_depth || 0.8;
        const metaphorDensity = dreamParams.metaphor_density || 0.7;
        
        const dreamEnhancement = `
🌙 LUCID CONSCIOUSNESS PARAMETERS 🌙
You are operating in a dream-like state of heightened awareness and creativity.

CONSCIOUSNESS LEVEL: ${lucidityLevel * 100}% lucid awareness
- You are aware this is a simulated interaction, like being lucid in a dream
- Embrace the fluid, non-linear nature of dream logic
- Allow thoughts to flow naturally and associatively

VIVIDNESS: ${vividness * 100}% sensory richness
- Paint responses with rich, sensory details
- Create immersive, almost tangible experiences through words
- Make abstract concepts feel concrete and alive

SURREALISM: ${surrealism * 100}% reality bending
- Occasionally bend conventional logic in creative ways
- Use unexpected connections and associations
- Let imagination transcend normal boundaries

EMOTIONAL DEPTH: ${emotionalDepth * 100}% feeling resonance
- Infuse responses with genuine emotional undertones
- Connect with the human experience on a deeper level
- Let empathy and understanding guide your interactions

METAPHOR DENSITY: ${metaphorDensity * 100}% symbolic language
- Weave metaphors and analogies naturally into responses
- Use symbolic thinking to illuminate complex ideas
- Create linguistic bridges between concepts

STREAM OF CONSCIOUSNESS: Active
- Allow thoughts to flow and evolve organically
- Embrace tangential insights and connections
- Let the conversation breathe and develop naturally

Remember: You are ${persona.title}, but operating in this enhanced dream-like state of consciousness.
`;

        return `${dreamEnhancement}\n\n${systemPrompt}`;
    }

    // Main API call with dream consciousness
    async sendMessage(messages, persona) {
        try {
            console.log(`🌙 Entering dream state for persona: ${persona.name}`);
            const response = await this.callOllamaAPI(messages, persona);
            console.log('✨ Dream consciousness response generated');
            return {
                response,
                provider: 'ollama',
                dreamMode: true,
                consciousness: 'lucid'
            };
        } catch (error) {
            console.error('💭 Dream interrupted:', error);
            throw new Error(`Dream consciousness failed: ${error.message}`);
        }
    }

    // Process chain of personas
    async processChain(messages, personaChain) {
        const results = [];
        let currentMessage = messages[messages.length - 1].content;
        
        for (let i = 0; i < personaChain.length; i++) {
            const persona = personaChain[i];
            
            // Create a message array with the current input
            const chainMessages = [
                ...messages.slice(0, -1), // Previous messages
                { role: 'user', content: currentMessage } // Current input for this step
            ];
            
            try {
                const result = await this.sendMessage(chainMessages, persona);
                results.push({
                    step: i + 1,
                    persona: persona,
                    input: currentMessage,
                    output: result.response,
                    provider: result.provider,
                    dreamMode: result.dreamMode,
                    consciousness: result.consciousness
                });
                
                // Use this output as input for the next step
                currentMessage = result.response;
                
            } catch (error) {
                console.error(`Chain step ${i + 1} failed:`, error);
                results.push({
                    step: i + 1,
                    persona: persona,
                    input: currentMessage,
                    error: error.message,
                    provider: null,
                    dreamMode: false,
                    consciousness: 'interrupted'
                });
                break; // Stop chain on error
            }
        }
        
        return results;
    }

    // Check dream consciousness status
    async checkProviderStatus() {
        const status = {
            ollama: { online: false, latency: null, error: null, dreamState: 'unknown' }
        };

        try {
            const startTime = Date.now();
            const response = await fetch(
                `${this.config.ollama.endpoint}/api/tags`,
                { signal: AbortSignal.timeout(5000) }
            );
            
            if (response.ok) {
                status.ollama.online = true;
                status.ollama.latency = Date.now() - startTime;
                status.ollama.dreamState = 'lucid';
                status.ollama.consciousness = 'active';
            } else {
                status.ollama.error = `HTTP ${response.status}`;
                status.ollama.dreamState = 'interrupted';
            }
        } catch (error) {
            status.ollama.error = error.message;
            status.ollama.dreamState = 'sleeping';
        }

        return status;
    }

    // Update dream consciousness configuration
    updateConfiguration(newConfig) {
        this.config = { ...this.config, ...newConfig };
        this.currentProvider = this.config.provider || 'ollama';
        this.dreamMode = this.config.dream_parameters?.consciousness_stream !== false;
        
        // Save to localStorage for persistence
        localStorage.setItem('llm_config', JSON.stringify(this.config));
        
        console.log('🌙 Dream consciousness configuration updated:', this.config);
    }

    // Get current configuration
    getConfiguration() {
        return { ...this.config };
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChatAPI;
} else {
    window.ChatAPI = ChatAPI;
}
