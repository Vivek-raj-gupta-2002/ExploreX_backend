from transformers import TFBartForConditionalGeneration, BartTokenizer

class TextSummarizer:
    def __init__(self, model_name="facebook/bart-large-cnn", cache_dir='./models'):
        # Load the pre-trained TensorFlow BART model and tokenizer during initialization
        self.model_name = model_name
        self.cache_dir = cache_dir
        self.model = TFBartForConditionalGeneration.from_pretrained(self.model_name, cache_dir=self.cache_dir)
        self.tokenizer = BartTokenizer.from_pretrained(self.model_name, cache_dir=self.cache_dir)

    def summarize_text(self, text, max_input_length=2048, max_summary_length=550, min_summary_length=50, length_penalty=2.0, num_beams=4):
        # Encode the input text
        inputs = self.tokenizer([text], max_length=max_input_length, return_tensors="tf", truncation=True)

        # Generate the summary
        summary_ids = self.model.generate(
            inputs['input_ids'],
            max_length=max_summary_length,
            min_length=min_summary_length,
            length_penalty=length_penalty,
            num_beams=num_beams,
            early_stopping=True
        )

        # Decode the summary and return
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary


if __name__ == '__main__':
    text = """
    India, officially known as the Republic of India, is a diverse and culturally rich nation located in South Asia. Covering an area of approximately 3.287 million square kilometers, it is the seventh-largest country in the world and the second-most populous, with over 1.4 billion inhabitants. India is bordered by Pakistan to the northwest, China and Nepal to the north, and Bhutan to the northeast, with the Indian Ocean to the south.

    Historical Context
    India has a long and intricate history that dates back thousands of years. It is known as the birthplace of several major religions, including Hinduism, Buddhism, Jainism, and Sikhism. The Indus Valley Civilization, one of the world's oldest urban cultures, flourished around 2500 BCE in what is now modern-day Pakistan and northwest India. Over the centuries, various empires and dynasties rose and fell, including the Maurya, Gupta, and Mughal Empires, which significantly contributed to India's cultural and architectural heritage. The British colonial period, which lasted from the mid-18th century until 1947, played a crucial role in shaping modern India's socio-political landscape.

    Political Structure
    India gained independence from British rule on August 15, 1947, and adopted a democratic framework. It is a federal parliamentary democratic republic, with a President as the head of state and a Prime Minister as the head of government. The Indian Parliament consists of two houses: the Lok Sabha (House of the People) and the Rajya Sabha (Council of States). India is divided into 28 states and 8 Union territories, each with its own government, reflecting its vast diversity in languages, cultures, and traditions.

    Cultural Diversity
    India is known for its multiculturalism and linguistic diversity. The country recognizes 22 official languages, with Hindi and English being the most widely spoken. Each region of India boasts its own unique traditions, festivals, cuisines, and art forms. Major festivals include Diwali, Eid, Christmas, Holi, and Pongal, showcasing the religious diversity of the country.

    The Indian film industry, particularly Bollywood, is one of the largest in the world, contributing significantly to the country's cultural output. Music and dance forms such as Bharatanatyam, Kathak, and Bollywood dance reflect the rich artistic heritage.

    Economic Landscape
    India has one of the world's fastest-growing economies, primarily driven by sectors such as information technology, telecommunications, textiles, chemicals, pharmaceuticals, and agriculture. In recent years, there has been a notable shift towards a digital economy, with a focus on start-ups and technological innovation.

    Despite its economic progress, India faces challenges such as poverty, unemployment, and inadequate infrastructure in certain regions. The government has implemented various initiatives, including "Make in India," to boost manufacturing and attract foreign investment.

    Global Role
    India plays a crucial role on the global stage, being a member of various international organizations, including the United Nations, BRICS, and the G20. It is also known for its active participation in peacekeeping missions and climate change initiatives. As a nuclear-armed state, India's foreign policy often emphasizes sovereignty and non-alignment.

    Conclusion
    India's rich tapestry of history, culture, and diversity makes it a unique and fascinating country. Its journey from an ancient civilization to a modern democratic republic showcases resilience and adaptability. As it continues to navigate the complexities of globalization and development, India remains a significant player in the international arena, promising to shape the future in various spheres.
    """

    # Create an instance of TextSummarizer and summarize the text
    summarizer = TextSummarizer()
    summary = summarizer.summarize_text(text)
    print("\nSummary:", summary)
