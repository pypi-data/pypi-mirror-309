# Example Plugin for DJ Press

[DJ Press](https://pypi.org/project/djpress/) is a blogging application for Django sites inspired by classic WordPress.

As of version 0.12, plugin support has been added, and this repository serves as an example of a simple plugin that
uses the following DJ Press hook to add some text before your blog posts:

- `pre_render_content` - this is called before the plain Markdown text has been converted to HTML.

## Plugin Development Steps

These are the specific steps that were followed to create this plugin. These steps were performed on a "Unix-like"
system but should work fine on Windows using WSL, macOS, or Linux. I use the `uv` tool
[from Astral](https://docs.astral.sh/uv/), but if you have another preferred tool, you should be able to follow along
and modify for your own use-case. You will also need a test Django site locally with DJ Press already installed and
configured. Creating this Django site is out of scope for these instructions; the assumption is that if you are
wanting to develop a DJ Press plugin, you will have already have access to a local Django site with DJ Press for
testing.

- Create a parent directory to store the plugin: `mkdir djpress-example-plugin`
- Initialise the project with a `pyproject.toml` file and recommended files and directories: `uv init --package`
- Remove the contents of `__init__.py` and update the `pyproject.toml` file with the following changes:
  - Remove the `project.scripts` section
  - Change the `requires-python` section to: `requires-python = ">=3.10"`. This is because DJ Press supports Python
    3.10 or newer, and so it is recommended that your plugin package does the same. If you are not planning to
    distribute your package to the public, then you can set this to your preferred version of Python.
  - Edit the rest of your file to suit your needs, e.g. `version`, `description`, `authors`, etc.
- Add `djpress` as a dependency of your project: `uv add djpress`
- Add any other dependencies that you require.
- Create the plugin module: `touch src/djpress_example_plugin/plugin.py`, and open in your favourite editor. This
  module does not *need* to be called `plugin.py`, but it makes the configuration and discovery of the plugin easier,
  so is highly recommended. The following steps are all done in `src/djpress_example_plugin/plugin.py`.
- Import `DJPressPlugin` which is the base class that this plugin will inherit from:
  `from djpress.plugins import DJPressPlugin`
- Create a new class called `Plugin` that inherits from `DJPressPlugin` - again, this does not *need* to be called
  `Plugin`, but makes configuration and discovery easier, so is highly recommended: `class Plugin(DJPressPlugin):`
- Give the plugin a name: `name = 'djpress_example_plugin'`. The name is used by DJ Press to discover related settings
  and while this could be anything you like, it is highly recommended to make this the same as the package name.
- Create a `setup` method that takes `registry` as an argument: `def setup(self, registry):`. The registry stores all
  the plugins that have registered with hooks. This is loaded at application start up.
- In the `setup` method, you register your plugin functionality with the appropriate plugin hook using the
  `register_hook` method from the `registry`, e.g. `registry.register_hook("pre_render_content", self.add_greeting)`
- Now create a method containing your plugin functionality: `def add_greeting(self, content):`. This method is passed
  `content` which is the plain Markdown text before it has been converted to HTML.
- For this example, we will also include some configurable text that can be stored in the `PLUGIN_SETTINGS` dictionary.
  Plugin-specific configuration is loaded as a dictionary called `config`. All that our silly example does, is add a
  greeting before the blog post content: `return f'Hello, {self.config.get("greeting_text")}!\n\n{content}'`
- That is the end of the plugin development. The next step is to install the plugin in a Django site to test that it
  works. To do this, you will need access to a test Django site locally. Navigate to the directory that stores your
  site and install your plugin package as an editable package. How to do this depends on your specific environment, but
  if you are using `uv` and your test site is in an adjacent directory, you could do something like this:
  `uv add --editable ../djpress-example-plugin`. The trick will be to get the path to your plugin correct.
- Once the package is installed, open your Django settings file in your favourite editor and add the following settings
  to the `DJPRESS_SETTINGS` configuration object:

    ```python
    # DJPress settings
    DJPRESS_SETTINGS = {
        # ... existing settings ...
        "PLUGINS": [
            "djpress_example_plugin",
        ],
        "PLUGIN_SETTINGS": {
            "djpress_example_plugin": {
                "greeting_text": "world",
            },
        },
    }
    ```

- If everything has worked, you should be able to run your Django site, open a blog post, and you'll see:
  `"Hello, world!"` before the blog post content. And if you view the source, you'll see that the text is wrapped in
  paragraph tags: `<p>Hello, world!</p>`. This is because the hook we used ran before the content was converted to
  HTML.
- You can now build your package and upload to PyPi so that others can use it in their projects. Before doing this, you
  should create a good README.md file with instructions on how to install and configure it, and what the plugin does.
  Publishing to PyPi is out of scope of these instructions but the
  [Python Packaging Guide](https://packaging.python.org/en/latest/) has some good information on how to get started.
  However, if you are already set up and ready to publish, `uv` has the ability to build your project: `uv build`, and
  then publish to PyPi: `uv publish`.
