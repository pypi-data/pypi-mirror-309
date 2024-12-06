from openai import OpenAI
import os

class SevenDeadlySwarms:
    def __init__(self):
        """Initialize the OpenAI client using the API key from the environment variable."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        self.client = OpenAI(api_key=api_key)

    def _process_content(self, content, swarms, action):
        """Processes content sequentially with the specified swarms."""
        for swarm_function in swarms:
            try:
                content = swarm_function(content, self.client)
            except Exception as e:
                content += f"\nError processing with {swarm_function.__name__}: {e}"
        return content

    def add_elements(self, content):
        """Adds elements of the seven deadly sins to the content."""
        return self._process_content(content, [
            self._add_pride,
            self._add_greed,
            self._add_wrath,
            self._add_envy,
            self._add_lust,
            self._add_gluttony,
            self._add_sloth
        ], action="add")

    def remove_elements(self, content):
        """Removes elements of the seven deadly sins from the content."""
        return self._process_content(content, [
            self._remove_pride,
            self._remove_greed,
            self._remove_wrath,
            self._remove_envy,
            self._remove_lust,
            self._remove_gluttony,
            self._remove_sloth
        ], action="remove")

    # Add functions
    def _add_pride(self, content, client):
        return client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Pride. Embellish the content."},
                      {"role": "user", "content": content}]
        ).choices[0].message.content

    def _add_greed(self, content, client):
        return client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Greed. Add elements of excess."},
                      {"role": "user", "content": content}]
        ).choices[0].message.content

    def _add_wrath(self, content, client):
        return client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Wrath. Add aggressive tones."},
                      {"role": "user", "content": content}]
        ).choices[0].message.content

    def _add_envy(self, content, client):
        return client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Envy. Add jealousy."},
                      {"role": "user", "content": content}]
        ).choices[0].message.content

    def _add_lust(self, content, client):
        return client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Lust. Add allure."},
                      {"role": "user", "content": content}]
        ).choices[0].message.content

    def _add_gluttony(self, content, client):
        return client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Gluttony. Add excess details."},
                      {"role": "user", "content": content}]
        ).choices[0].message.content

    def _add_sloth(self, content, client):
        return client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Sloth. Add apathy."},
                      {"role": "user", "content": content}]
        ).choices[0].message.content

    # Remove functions
    def _remove_pride(self, content, client):
        return client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Pride. Remove grandiosity."},
                      {"role": "user", "content": content}]
        ).choices[0].message.content

    def _remove_greed(self, content, client):
        return client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Greed. Remove excess."},
                      {"role": "user", "content": content}]
        ).choices[0].message.content

    def _remove_wrath(self, content, client):
        return client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Wrath. Remove aggression."},
                      {"role": "user", "content": content}]
        ).choices[0].message.content

    def _remove_envy(self, content, client):
        return client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Envy. Remove jealousy."},
                      {"role": "user", "content": content}]
        ).choices[0].message.content

    def _remove_lust(self, content, client):
        return client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Lust. Remove seduction."},
                      {"role": "user", "content": content}]
        ).choices[0].message.content

    def _remove_gluttony(self, content, client):
        return client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Gluttony. Remove excess detail."},
                      {"role": "user", "content": content}]
        ).choices[0].message.content

    def _remove_sloth(self, content, client):
        return client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are Sloth. Remove apathy."},
                      {"role": "user", "content": content}]
        ).choices[0].message.content
