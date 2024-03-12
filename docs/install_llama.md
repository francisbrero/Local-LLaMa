# Alternative version
[source](https://gist.github.com/cedrickchee/e8d4cb0c4b1df6cc47ce8b18457ebde0)


# 0. install dependencies
```bash
brew install pkgconfig cmake
```


# 1. Download official facebook model
The github location for facebook llama 2 is below: https://github.com/facebookresearch/llama

Open terminal and clone the repository:

```bash
cd ~/Documents
git clone git@github.com:facebookresearch/llama.git
```
To use the facebook model for free (unless you are servicing 700 million users), you need to request a [new download link from Facebook](https://ai.meta.com/resources/models-and-libraries/llama-downloads/). Once you have agreed with the terms, an email will be sent to you with a download link (typically a couple of days, subsequent requests will take seconds). The link will only be valid for 24 hours, but you can re-request, to avoid hassle, just download the models you want within 24 hours.

To download the model, it is fairly easy, just cd to you repo and run download.sh (you may need to do chmod on download.sh):

```bash
cd ~/Documents/llama
./download.sh
```
You don’t need to download all, personally I think 7B performs pretty well. Depends on the tasks, you may also want to download 7B-chat, which is more tuned for conversation. 
I am finding for zero shot 7B-chat generate better results for me.

# 2. Use llama.cpp to convert and quantize the downloaded models
The model you have download will still need to be converted and quantized for work. Quantization is a method to reduce the accuracy of the weights to minimize memory and compute. Typically the models may be trained with high precision float 32, we can lower it to lower bits to cater for the spec of our Macbooks.

The first step is to clone llama.cpp repostory (https://github.com/ggerganov/llama.cpp):
```bash
cd ~/Documents
git clone git@github.com:ggerganov/llama.cpp.git
```
Then install brew and xcode command line tools and make the binary:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

xcode-select –install 
```
```bash
brew install pkgconfig cmake
```

```bash
cd llama.cpp

LLAMA_METAL=1 make
```

The next step is to convert download model to the ggml format (https://ggml.ai/), the following create a virtual environment, install the required packages and convert the llama 7b chat model:

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

```bash
pip install --pre torch torchvision --extra-index-url https://download.pytorch.org/whl/nightly/cpu
```

```bash
python convert.py ../llama/llama-2-7b-chat 1
```

This will generate the another file under the model you’ve downloaded on facebook. I didn’t generate a name as I was lazy, the filename should look like ggml-model-f16.gguf.

To quantize the model (make it smaller), the following quantize the model from F16 to 4 bit integer (and suprisingly it is still performing well):
```bash
./quantize ../llama/llama-2-7b-chat/ggml-model-f16.gguf ../llama/llama-2-7b-chat/ggml-model-f16_q4_0.gguf q4_0
```
It is almost done, and you can see a significant size reduction from 14gigs to 3gigs.

## test the model you've built
```bash
./main -m ../llama/llama-2-7b-chat/ggml-model-f16_q4_0.gguf \
        -t 8 \
        -n 128 \
        -p 'A Kudu is a form of antelope '
```
This should feel magical! LLaMa is running on your Macbook!


# 3. Use python binding via llama-cpp-python
To use it in python, we can install another helpful package. The installation of package is same as any other package, but make sure you enable metal.
```bash
CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install llama-cpp-python
```
## Using the model
To use the model, I have created a sample code below. The prompt instruction is what I have dugged up on reddit. 
```bash
from llama_cpp import Llama

model_path = "~/Documents/llama/llama-2-7b-chat/ggml-model-f16_q4_0.gguf"
model = Llama(model_path = model_path,       
              , temperature=0.75
              , max_tokens=2000
              , n_gqa=8 # Number of GPUs to use
              , top_p=1
              , verbose=True # Verbose is required to pass to the callback manager
              , f16_kv=True  # MUST set to True, otherwise you will run into problem after a couple of calls
              , n_ctx=2048 # context window size
              , n_batch=512 # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.
              , n_gpu_layers=1 # Metal set to 1 is enough.
              , use_mlock = True # enable memory lock so not swap
              )        


prompt = """
[INST]<<SYS>>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.

What is the best way to learn programming?
[/INST]
"""

output = model(prompt = prompt, max_tokens = 120, temperature = 0.2)
output
```
```JSON
{'id': 'cmpl-92ec0995-11e5-4eeb-9311-98d0f23c4885',
 'object': 'text_completion',
 'created': 1691921343,
 'model': './models/ggml-llama-7b-chat-q4_0.bin',
 'choices': [{'text': 'Thank you for asking! Learning programming can be an exciting and rewarding journey, and there are several great ways to get started. Here are some recommendations:\n1. Online Courses: Websites such as Codecademy, Coursera, and Udemy offer a wide range of programming courses, from beginner to advanced levels. These courses are often interactive and include practical exercises to help you learn by doing.\n2. Books: If you prefer learning through reading, there are many excellent books on programming available. "Code Complete" by Steve McConnell, "C',
   'index': 0,
   'logprobs': None,
   'finish_reason': 'length'}],
 'usage': {'prompt_tokens': 143,
  'completion_tokens': 120,
  'total_tokens': 263}}
```
To use langchain (api reference: https://api.python.langchain.com/en/latest/llms/langchain.llms.llamacpp.LlamaCpp.html):
```bash
from langchain.llms import LlamaCpp
llm = LlamaCpp(model_path=model_path)

llm(prompt)
```

Note:
The console log will show the following log to indicate Metal was enable properly.
```bash
ggml_metal_init: allocating
ggml_metal_init: found device: Apple M2
```