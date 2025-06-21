from app.services import openai as target


def test_completion() -> None:
    messages = [
        target.Prompt(
            role="system",
            content=[
                target.PromptContent(type="text", text="情報を見つけるのに役立つ AI アシスタントです。")
            ]
        ),
        target.Prompt(
            role="user",
            content=[
                target.PromptContent(type="text", text="こんにちは")
            ]
        ),
    ]

    target.completion(messages=messages)
    assert True  # Replace with actual assertions based on expected behavior
