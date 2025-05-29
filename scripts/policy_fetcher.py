from dotenv import load_dotenv
import os
import requests
import pandas as pd
import time

load_dotenv()
API_KEY = os.getenv("YOUTH_API_KEY")
BASE_URL = "https://www.youthcenter.go.kr/go/ythip/getPlcy"

def fetch_policies(page_limit=50, save_path="data/raw/fetched_policies.csv"):
    print("API_KEY 확인:", API_KEY)
    all_policies = []
    for page in range(1, page_limit + 1):
        params = {
            "apiKeyNm": API_KEY,
            "pageNum": page,
            "pageSize": 100,
            "rtnType": "json",
            "pageType": "1"
        }
        try:
            res = requests.get(BASE_URL, params=params, timeout=10)
            print("요청 URL:", res.url)
            print("응답 상태 코드:", res.status_code)
            print("응답 텍스트 앞부분:", res.text[:300])

            res.raise_for_status()
            result = res.json().get("result", {})
            data = result.get("youthPolicyList", [])
            
            if not data:
                print(f"📭 No data on page {page}, stopping.")
                break
            all_policies.extend(data)
            print(f"✅ Page {page}: {len(data)} policies fetched.")
            time.sleep(0.3)  # 살짝 대기: 과한 요청 방지

        except Exception as e:
            print(f"❌ Error on page {page}: {e}")
            break

    df = pd.DataFrame(all_policies)
    df.to_csv(save_path, index=False, encoding="utf-8-sig")
    print(f"\n🎉 총 {len(df)}개 정책 저장 완료 → {save_path}")

if __name__ == "__main__":
    fetch_policies()
