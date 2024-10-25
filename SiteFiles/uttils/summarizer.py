import os
from openai import AzureOpenAI
import google.generativeai as genai
from django.conf import settings

class TextAnalyzer:
    """
    A class to analyze text using either Azure OpenAI or Bard AI based on user preference.
    """
    
    def __init__(self, use_azure=False):
        """
        Initializes the TextAnalyzer with either Azure OpenAI or Bard AI.
        :param use_azure: If True, uses Azure OpenAI, otherwise uses Bard AI.
        """
        self.use_azure = use_azure

        if self.use_azure:
            # Initialize Azure OpenAI client using environment variables
            self.client = AzureOpenAI(
                azure_endpoint=settings.ENDPOINT,
                api_key=settings.OPENAI_API_KEY,
                api_version=settings.API_VERSION
            )
            self.model = settings.MODEL
        else:
            # Bard AI configuration
            genai.configure(settings.BARD_API)

    def _call_azure_openai(self, prompt):
        """
        Calls Azure OpenAI to get a response based on the user prompt.
        :param prompt: The prompt to be sent to Azure OpenAI.
        :return: The response from Azure OpenAI.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. && also show positivity in every aspects"},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling Azure OpenAI API: {str(e)}")
            return None

    def _call_bard_ai(self, prompt):
        """
        Calls Bard AI to get a response based on the user prompt.
        :param prompt: The prompt to be sent to Bard AI.
        :return: The response from Bard AI.
        """
        try:
            response = genai.GenerativeModel("gemini-1.5-pro").generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Bard API: {str(e)}")
            return None

    def summarize_text(self, text, word_limit=100, max_input_length=2000):
        """
        Summarizes the input text with a specified word limit.
        :param text: The text to summarize.
        :param word_limit: Maximum number of words for the summary.
        :param max_input_length: Maximum input text length.
        :return: The summary as a string.
        """
        prompt = f"Summarize the following text in {word_limit} words:\n\n{text[:max_input_length]}"
        return self._call_api(prompt)

    def analyze_personality(self, text, word_limit=20, max_input_length=2000):
        """
        Analyzes the personality of the user based on the text.
        :param text: The text to analyze.
        :param word_limit: Maximum number of words for the analysis.
        :param max_input_length: Maximum input text length.
        :return: The personality analysis as a string.
        """
        prompt = f"Based on the following text, describe the personality of the person in {word_limit} words :\n\n{text[:max_input_length]}"
        return self._call_api(prompt)

    def describe_mood(self, text, word_limit=25, max_input_length=2000):
        """
        Describes the mood expressed in the text.
        :param text: The text to analyze.
        :param word_limit: Maximum number of words for the mood description.
        :param max_input_length: Maximum input text length.
        :return: The mood description as a string.
        """
        prompt = f"Describe the mood expressed in the following text in {word_limit} words in the form of bullitons:\n\n{text[:max_input_length]}"
        return self._call_api(prompt)

    def suggest_tasks(self, text, word_limit=25, max_input_length=2000):
        """
        Suggests tasks based on the text analysis.
        :param text: The text to analyze.
        :param word_limit: Maximum number of words for the task suggestions.
        :param max_input_length: Maximum input text length.
        :return: Suggested tasks as a string.
        """
        prompt = f"Based on the following text, suggest 3-4 tasks the person should focus on {word_limit} words and only give headings of one word and the tasks should be physical or real don't describe them only 4 activity and dont use sub points:\n\n{text[:max_input_length]}"
        return self._call_api(prompt)

    def _call_api(self, prompt):
        """
        Calls either Azure OpenAI or Bard AI based on the user's preference.
        :param prompt: The prompt to be processed.
        :return: The API response as a string.
        """
        if self.use_azure:
            return self._call_azure_openai(prompt)
        else:
            return self._call_bard_ai(prompt)


# Example usage
if __name__ == '__main__':
    text = """
    India, officially known as the Republic of India, is a diverse and culturally rich nation located in South Asia.
    Covering an area of approximately 3.287 million square kilometers, it is the seventh-largest country in the world 
    and the second-most populous, with over 1.4 billion inhabitants. India is bordered by Pakistan to the northwest, 
    China and Nepal to the north, and Bhutan to the northeast, with the Indian Ocean to the south.
    
    India gained independence from British rule on August 15, 1947, and adopted a democratic framework.
    It is a federal parliamentary democratic republic, with a President as the head of state and a Prime Minister 
    as the head of government. The Indian Parliament consists of two houses: the Lok Sabha and the Rajya Sabha.
    """

    # Create an instance of TextAnalyzer using Azure OpenAI
    azure_analyzer = TextAnalyzer(use_azure=True)
    azure_summary = azure_analyzer.summarize_text(text, word_limit=350)
    print("\nAzure Summary:", azure_summary)

    # Create an instance of TextAnalyzer using Bard AI
    bard_analyzer = TextAnalyzer(use_azure=False)
    bard_summary = bard_analyzer.summarize_text(text, word_limit=350)
    print("\nBard Summary:", bard_summary)
