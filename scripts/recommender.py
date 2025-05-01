import pandas as pd

def calculate_score_and_reason(policy_row, user):
    score = 0
    reasons = []

    if policy_row["min_age"] <= user["age"] <= policy_row["max_age"]:
        score += 30
        reasons.append("나이 조건 일치 (+30)")
    else:
        reasons.append("나이 조건 불일치")

    if user["income"] <= policy_row["income_ceiling"]:
        score += 25
        reasons.append("소득 조건 일치 (+25)")
    else:
        reasons.append("소득 초과")

    if user["region"] in policy_row["target_region"]:
        score += 20
        reasons.append("지역 조건 일치 (+20)")
    else:
        reasons.append("지역 불일치")

    if user["job_status"] in str(policy_row["job_status"]).split(","):
        score += 15
        reasons.append("고용 상태 일치 (+15)")
    else:
        reasons.append("고용 상태 불일치")

    if policy_row["household_type"] == "무관" or policy_row["household_type"] == user["household_type"]:
        score += 10
        reasons.append("가구 형태 일치 (+10)")
    else:
        reasons.append("가구 형태 불일치")

    return pd.Series([score, " / ".join(reasons)], index=["recommendation_score", "reason"])


def recommend(user_input: dict, policy_df: pd.DataFrame) -> pd.DataFrame:
    """
    사용자 입력과 정책 데이터프레임을 받아 추천 결과를 반환합니다.
    
    Args:
        user_input (dict): 사용자의 프로필 (age, income, region, job_status, household_type)
        policy_df (pd.DataFrame): 정책 리스트

    Returns:
        pd.DataFrame: 점수 및 추천 이유가 포함된 추천 결과
    """
    result = policy_df.copy()
    result[["recommendation_score", "reason"]] = result.apply(
        lambda row: calculate_score_and_reason(row, user_input),
        axis=1
    )
    return result.sort_values(by="recommendation_score", ascending=False).reset_index(drop=True)
