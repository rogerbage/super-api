import openai
from openai import OpenAI
import tiktoken
import os
import maritalk
import json
import time

#########################################################
class chats:

    def basicOpenai(input):
        #-----------------------------------------------------#
        # basicOpenai faz uma requisição para a openai
        # usando o modelo gpt-3.5-turbo
        #-----------------------------------------------------#

        client = OpenAI()
        messages=[
            { "role": "system", "content": "Você é um robô especialista em processamento de texto."},
            { "role": "user", "content": input},
        ]

        input_tokens = chats.count_tokens(messages)
        print("\n\nINPUT TOKENS: ", input_tokens, "\n\n")
        max_tokens = int(16000 - (input_tokens + (input_tokens*0.2)))
        
        if (max_tokens < 512):
            return "Seu texto excede o tamanho máximo do prompt."
        
        client
        tentativas = 0
        resposta = ""
        seed=500
        
        while tentativas < 10:
            try:
                tentativas += 1
                #max_tokens=max_tokens,
                chat_completion = client.chat.completions.create(
                    model="gpt-3.5-turbo-16k",
                    temperature=0,
                    messages=messages,
                    seed=seed,
                )
                print("\nCHAT COMPLETION: ", chat_completion, "\n\n")
                resposta = chat_completion.choices[0].message.content
                return(resposta)
                                        
                
            except openai.APIError as e:
                print(f"OpenAI API error: {e}")
                time.sleep(tentativas)
                pass
            except Exception as e:
                print(f"Erro não previsto: {e}")
                time.sleep(tentativas)
                pass
        return False      
        
    ########################################################################


    #########################################################################
    def basicMaritalk(input):
        model = maritalk.MariTalk(
            key=os.getenv('MARITALK_API_KEY', ''),
            model="sabia-2-medium",
        )
        prompt = input

        tentativas = 0
        while tentativas < 10:
            tentativas += 1
            try:
                response = model.generate(
                    prompt
                )
                print(response)
                return response['answer']
            except Exception as e:
                print(f"Erro não previsto: {e}")
                time.sleep(tentativas)
                pass

        return False
    ########################################################################

    ########################################################################
    def count_tokens(messages, model="gpt-3.5-turbo-0301"):
        #----------------------------------------------------------#
        # num_tokens_from_messages retorna o número de tokens de um texto
        # para calcular tamanho de prompt com a API da openai.
        #----------------------------------------------------------#
        """Returns the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo":
            print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
            return chats.count_tokens(messages, model="gpt-3.5-turbo-0301")
        elif model == "gpt-4":
            print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
            return chats.count_tokens(messages, model="gpt-4-0314")
        elif model == "gpt-3.5-turbo-0301":
            tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif model == "gpt-4-0314":
            tokens_per_message = 3
            tokens_per_name = 1
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens
    #######################################################################



    #######################################################################
    def modeloRefinaResposta(slices, prompt):
        concat = ""
        concata = []
        melhor_resposta = ""

        for slice in slices:
            query = (
                f"{prompt}"
                f"```"
                f"{slice}"
            )
            resposta = chats.basicOpenai(query)
            concat = concat + resposta + "\n\n"
            concata.append(resposta)
            if ( len(concata) == 1):
                melhor_resposta = resposta
            else:
                refina_prompt = (
                    f"Uma pergunta foi feita para um documento grande. Dividimos o documento em várias trechos."
                    f"No item 'Resposta Final' temos a resposta baseada nos trechos anteriores."
                    f"Baseado na 'Pergunta' e na 'Resposta do trecho atual', vamos melhorar a 'Resposta Final."
                    f"Faça alterações na 'Resposta Final' apenas se tiver certeza. Evite perder informações da 'Resposta Final'."
                    f"Refine a 'Resposta Final' e adicione novas informações encontradas se forem relevantes."
                    f"Retorne apenas o texto da 'Resposta Final' melhorada."
                    f"\n\n"
                    f"Pergunta: `{prompt}`"
                    f"\n\n"
                    f"Resposta Final: {melhor_resposta}"
                    f"\n\n"
                    f"Resposta do trecho atual: {resposta}"
                )

                melhor_resposta = chats.basicOpenai(refina_prompt)
            
        return (melhor_resposta)
#######################################################################


    #######################################################################
    def modeloConcatenaResposta(slices, prompt):
        concata = []
        melhor_resposta = ""
        slice_count = 0
        for slice in slices:
            slice_count += 1
            chunk = {
                "chunk": slice_count,
                "total_chunks": len(slices),
                "pergunta_1": prompt,
                "texto": slice,  
            }
            query = (
                f"Uma pergunta foi feita para um documento grande. O documento foi dividido em chunks.\n"
                f"Responda a pergunta_1 abaixo baseado no texto fornecido, levando em conta que o texto é uma parte do documento.\n"
                f"Responda apenas se houver uma resposta coerente para o trecho de texto. Se não houver resposta, retorne apenas um traço ( - )\n"
                f"\n######\n"
                f"{json.dumps(chunk)}"
            )


            resposta = chats.basicOpenai(query)

            concata.append({
                "chunk": slice_count,
                "total_chunks": len(slices),
                "resposta": resposta, 
            })
            
        concat_prompt = (
            f"Dividimos o documento em várias trechos.\n"
            f"Para cada trecho fizemos a mesma pergunta, e registramos a resposta.\n"
            f"As respostas são do mesmo documento, então precisamos juntar as respostas de todos os trechos.\n"
            f"Baseado em todas as respostas, crie uma resposta única.\n"
            f"Remova as respostas que não condizem com a pergunta."
            f"Retorne apenas a resposta a pergunta abaixo, e nada mais.\n"
            f"\n###########\n"
            f"\nPergunta: {prompt}\n"
            f"\n\n###########\n"
            f"\nRespostas: "
            f"{json.dumps(concata)}\n\n"
        )

        print(concat_prompt)

        concata_resposta = chats.basicOpenai(concat_prompt)
            
        return (concata_resposta)
#######################################################################