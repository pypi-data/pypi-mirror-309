from djpress.plugins import DJPressPlugin


class Plugin(DJPressPlugin):
    name = "djpress_example_plugin"

    def setup(self, registry):
        registry.register_hook("pre_render_content", self.add_greeting)

    def add_greeting(self, content):
        return f'Hello, {self.config.get("greeting_text")}!\n\n{content}'
