from pathlib import Path
from pydantic_core import from_json, to_json

from agents import (Runner,
                    TResponseInputItem,
                    InputGuardrailTripwireTriggered
                    )


from agents.voice import (
    AudioInput,
    SingleAgentVoiceWorkflow,
    SingleAgentWorkflowCallbacks,
    VoicePipeline
)

from audio_utils import AudioPlayer, gen_empty_audio, record_audio
from data_models import RestaurantMenu, RestaurantOrder, OrderState
from restaurant_agents import triage_agent, restaurant_menu_extractor_agent


class WorkflowCallbacks(SingleAgentWorkflowCallbacks):
    def on_run(self, workflow: SingleAgentVoiceWorkflow, transcription: str) -> None:
        print(f'[debug] on_run called with transcription: {transcription}')


class ChatClient(object):
    def __init__(self, voice=False):
        self.current_agent = triage_agent
        self.input_items: list[TResponseInputItem] = []
        self.welcome_message = 'Welcome to our restaurant! How may I help you?'
        self.goodbye_message = 'Thanks for your custom. We hope to see you again.'
        self.restaurant_menu = self._load_menu()
        self.voice = voice

    @staticmethod
    def _load_menu() -> RestaurantMenu:
        menu_path = Path('data/bardo_menu.json')
        if menu_path.exists():
            with open(menu_path, 'rb') as f:
                menu_json = f.read()
            return RestaurantMenu.model_validate(from_json(menu_json))

    async def run(self):
        if not self.restaurant_menu:
            menu_raw_text_file = Path('data/bardo_menu.txt')
            with open(menu_raw_text_file, 'rb') as f:
                menu_text = f.read()
            input_items = [{'content': f'Parse the following menu text: {menu_text}',
                            'role': 'user'}]
            menu_parse_result = await Runner.run(restaurant_menu_extractor_agent,
                                                 input_items)
            self.restaurant_menu = menu_parse_result.final_output
            save_menu_path = Path('data/bardo_menu.json')
            menu_json = to_json(self.restaurant_menu,
                                indent=4)
            with open(save_menu_path, 'wb') as f:
                f.write(menu_json)
        print(self.welcome_message)
        restaurant_order = RestaurantOrder()

        if self.voice:
            voice_pipeline = VoicePipeline(
                workflow=SingleAgentVoiceWorkflow(self.current_agent,
                                                  callbacks=WorkflowCallbacks())
            )

        while True:
            try:
                input_items = []

                if self.voice:
                    audio_input = AudioInput(buffer=record_audio())
                else:
                    input_items = [{'content': input('User: '),
                                    'role': 'user'}]

                if self.current_agent.name in ['Restaurant Menu', 'Food Orderer']:
                    system_prompt = {'content': f'Get all food item information from the following menu only: {to_json(self.restaurant_menu)}',
                                     'role': 'system'}
                    input_items.append(system_prompt)

                if self.voice:
                    result = await voice_pipeline.run(audio_input)
                    with AudioPlayer() as player:
                        async for event in result.stream():
                            if event.type == 'voice_stream_event_audio':
                                player.add_audio(event.data)
                        player.add_audio(gen_empty_audio(seconds=1))
                else:
                    result = await Runner.run(self.current_agent, input_items, context=restaurant_order)
                    print(f'{result.last_agent.name}: {result.final_output}')

                self.current_agent = result.last_agent
                if restaurant_order.order_state == OrderState.DONE_WITH_ORDER:
                    self.current_agent = triage_agent
            except KeyboardInterrupt:
                print(self.goodbye_message)
                exit()
            except InputGuardrailTripwireTriggered as triggered_tripwire:
                print(f'Guardrail agent: {triggered_tripwire.guardrail_result.output.output_info.reasoning}')
                self.current_agent = triage_agent
