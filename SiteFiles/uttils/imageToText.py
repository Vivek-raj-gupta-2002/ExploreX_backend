from transformers import TFVisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer, pipeline
from PIL import Image
import tensorflow as tf

class ImageToText:
    def __init__(self, model_name="nlpconnect/vit-gpt2-image-captioning", max_length=16, num_beams=4, cache_dir='./models'):
        # Load the PyTorch weights into the TensorFlow model
        self.model = TFVisionEncoderDecoderModel.from_pretrained(model_name, cache_dir=cache_dir, from_pt=True)
        self.feature_extractor = ViTImageProcessor.from_pretrained(model_name, cache_dir=cache_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        
        # Set device (use GPU if available)
        self.device = "GPU" if tf.config.list_physical_devices('GPU') else "CPU"
        
        # Generation settings
        self.gen_kwargs = {"max_length": max_length, "num_beams": num_beams}
    
    def load_image(self, image_path):
        """Load and preprocess an image"""
        image = Image.open(image_path)
        if image.mode != "RGB":
            image = image.convert("RGB")
        return image
    
    def predict_caption(self, image_paths):
        """Generate captions for given image paths"""
        # Load and process images
        images = [self.load_image(image_path) for image_path in image_paths]
        pixel_values = self.feature_extractor(images=images, return_tensors="tf").pixel_values
        
        # Generate captions using TensorFlow operations
        output_ids = self.model.generate(pixel_values, **self.gen_kwargs)
        captions = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        captions = [caption.strip() for caption in captions]
        return captions
    
    @staticmethod
    def predict_with_pipeline(image_path_or_url):
        """Simpler pipeline-based approach for image captioning"""
        image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
        return image_to_text(image_path_or_url)

# Usage Example:

if __name__ == '__main__':
    # Full model-based approach
    image_captioner = ImageToText()
    captions = image_captioner.predict_caption(['download.jpeg'])
    print(captions)
