# luminagen_ai/llm.py
from llama_cpp import Llama

# This global variable will hold the loaded model so we don't reload it
llm_model = None

def load_model(model_path: str):
    """
    Loads the LLaMA GGUF model from the specified path.
    Offloads all possible layers to the GPU for maximum performance on Apple Silicon.
    """
    global llm_model
    if llm_model is None:
        print("INFO: Loading LLaMA model... This may take a moment.")
        llm_model = Llama(
            model_path=model_path,
            n_ctx=2048,        # The maximum context size
            n_gpu_layers=-1,   # <<< THIS IS THE KEY for your M4 Pro. -1 offloads all layers to the GPU.
            verbose=False
        )
        print("INFO: LLaMA model loaded successfully.")

def generate_text(prompt: str) -> str:
    """Generates text using the loaded LLaMA model."""
    if llm_model is None:
        raise Exception("Model not loaded. Please call load_model() first.")

    output = llm_model(
        prompt,
        max_tokens=512,      # Max number of tokens to generate
        stop=["Q:"],         # <<< FIX: Removed "\n" to allow multi-line generation for paragraphs.
        echo=False           # Don't echo the prompt in the output
    )

    return output['choices'][0]['text'].strip()