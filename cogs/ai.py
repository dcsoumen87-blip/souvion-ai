async def generate_response(self, question, guild_id=None):
    prompt = self.build_prompt(question, guild_id)

    models = [
        "gemini-3.8-flash",
        "gemini-3.7-flash",
    ]

    last_error = None

    for model_name in models:
        for attempt in range(3):
            try:
                print(
                    f"[GEMINI] Model={model_name} "
                    f"Attempt={attempt + 1}/3"
                )

                response = await asyncio.to_thread(
                    ai.models.generate_content,
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens=800
                    )
                )

                answer = response.text

                if not answer:
                    return "Sorry, I could not generate a response."

                print(f"[GEMINI] Success using {model_name}")
                return answer.strip()

            except Exception as error:
                last_error = error
                error_text = str(error)

                print("=" * 50)
                print(
                    f"GEMINI ERROR | "
                    f"MODEL={model_name} | "
                    f"ATTEMPT={attempt + 1}/3"
                )
                print(error)
                print("=" * 50)

                is_temporary = (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                    or "500" in error_text
                    or "429" in error_text
                )

                if is_temporary and attempt < 2:
                    wait_time = 2 ** attempt
                    print(
                        f"[GEMINI] Retrying {model_name} "
                        f"in {wait_time}s..."
                    )
                    await asyncio.sleep(wait_time)
                    continue

                break

        print(
            f"[GEMINI] {model_name} unavailable. "
            f"Trying next model..."
        )

    raise last_error
