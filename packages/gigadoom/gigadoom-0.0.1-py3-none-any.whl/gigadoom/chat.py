import requests
import json
import uuid


def get_access_token(client_secret, scope="GIGACHAT_API_PERS"):
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    data = {"scope": scope}
    req_id = uuid.uuid4()
    headers = {
        "Authorization": f"Bearer {client_secret}",
        "RqUID": str(req_id),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.request("POST", url, headers=headers, data=data, verify=False)
    print(response.text)
    res = json.loads(response.text)

    return res["access_token"], res["expires_at"]


def get_models(acc_token):
    url = "https://gigachat.devices.sberbank.ru/api/v1/models"
    headers = {
        "Authorization": f"Bearer {acc_token}",
    }
    response = requests.request("GET", url, headers=headers, verify=False)
    print(response.text)
    res = json.loads(response.text)

    return res["data"]


def get_completion(query, acc_token, history=[], model="GigaChat:latest", temperature=0.5, top_p=0.95):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {acc_token}",
        "Content-Type": "application/json",
    }

    history.append({"content": query, "role": "user"})
    payload = json.dumps(
        {
            "messages": history,
            "model": model,
            "temperature": temperature,
            "top_p": top_p,
        }
    )

    response = requests.request(
        "POST", url, headers=headers, data=payload, verify=False
    )
    print(response.text)
    res = json.loads(response.text)

    print(res)

    history.append(res["choices"][-1]["message"])

    return res["choices"][-1]["message"]["content"], history, res["usage"]