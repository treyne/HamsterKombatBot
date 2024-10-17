from typing import Any, Union, Dict, List, Optional, Tuple

import aiohttp

import re
from bot.api.http import make_request, handle_error


async def get_nuxt_builds(http_client: aiohttp.ClientSession) -> Dict[Any, Any]:
    base_url = "https://hamsterkombatgame.io/_nuxt/"
    entry_js_url = base_url + "entry.BlVsFSc5.js"
    response_text = None
    try:
        # Получаем содержимое entry.BlVsFSc5.js
        response_text = await make_request(
            http_client,
            'GET',
            entry_js_url,
            None,
            'getting entry JS file'
        )

        # Ищем buildId в содержимом entry.js
        pattern = r'buildId\s*:\s*"([a-f0-9\-]+)"'
        match = re.search(pattern, response_text)

        if match:
            build_id = match.group(1)
            build_meta_url = f"{base_url}builds/meta/{build_id}.json"
            print(f"Build meta URL: {build_meta_url}")

            # Запрашиваем build meta JSON по динамически сформированной ссылке
            response_json = await make_request(
                http_client,
                'GET',
                build_meta_url,
                None,
                'getting Nuxt Builds'
            )
            return response_json
        else:
            print("Build ID not found in entry.js file!")
            return {}

    except Exception as error:
        await handle_error(error, response_text, 'getting Nuxt Builds')
        return {}
