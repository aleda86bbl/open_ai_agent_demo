from agents import Runner, InputGuardrailTripwireTriggered

class TextChatClient(object):
    def __init__(self, agent):
        self.agent = agent
        self.welcome_message = 'Welcome to our restaurant! How may I help you?'
        self.goodbye_message = 'Thanks for your custom. We hope to see you again.'

    async def run(self):
        print(self.welcome_message)
        while True:
            try:
                print('User:')
                user_input = input()
                result = await Runner.run(self.agent, user_input)
                print(f'{result.last_agent.name}:')
                print(result.final_output)
            except KeyboardInterrupt:
                print(self.goodbye_message)
                exit()
            except InputGuardrailTripwireTriggered as triggered_tripwire:
                print('Guardrail agent:')
                print(triggered_tripwire.guardrail_result.output.output_info.reasoning)
        
