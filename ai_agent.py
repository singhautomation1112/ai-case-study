from langchain_openai import ChatOpenAI

from tools import (
    generate_patient_record,
    update_patient_record,
    validate_integration_contract,
    run_smoke_test,
    system_health_check,
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


def ask_agent(query: str):

    query = query.lower()

    if "generate" in query or "patient" in query:
        return generate_patient_record(
            "Test Patient",
            "1990-01-01",
            "default"
        )

    elif "update" in query:
        return update_patient_record(
            [],
            "patient_id",
            "New Name",
            "NewTenant"
        )

    elif "validate" in query:
        return validate_integration_contract(
            "INS1234",
            1000
        )

    elif "smoke" in query:
        return run_smoke_test(
            [
                {
                    "patient_id": "1",
                    "tenant_id": "default"
                }
            ],
            "default"
        )

    elif "health" in query:
        return system_health_check()

    else:
        return {
            "message": "Sorry, I couldn't understand the request."
        }