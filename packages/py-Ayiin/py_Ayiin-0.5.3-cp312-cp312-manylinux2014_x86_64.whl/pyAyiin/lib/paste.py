import json
import requests
import pyAyiin


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "content-type": "application/json",
}


class Paste:
    async def p_paste(self: "pyAyiin.pyAyiin", message, extension=None):
        siteurl = "https://pasty.lus.pm/api/v1/pastes"
        data = {"content": message}
        try:
            response = requests.post(
                url=siteurl,
                data=json.dumps(data),
                headers=headers)
        except Exception as e:
            return {"error": str(e)}
        if response.ok:
            response = response.json()
            purl = (
                f"https://pasty.lus.pm/{response['id']}.{extension}"
                if extension
                else f"https://pasty.lus.pm/{response['id']}.txt"
            )
            try:
                await self.send_message(
                    self.BOTLOG_CHATID,
                    f"**You have created a new paste in pasty bin.** Link to pasty is [here]({purl}). You can delete that paste by using this token `{response['deletionToken']}`",
                )
            except Exception as e:
                self.log.info(str(e))
            return {
                "url": purl,
                "raw": f"https://pasty.lus.pm/{response['id']}/raw",
                "bin": "Pasty",
            }
        return {"error": "Unable to reach pasty.lus.pm"}


    async def s_paste(self: "pyAyiin.pyAyiin", message, extension="txt"):
        siteurl = "https://spaceb.in/api/v1/documents/"
        try:
            response = requests.post(
                siteurl, data={"content": message, "extension": extension}
            )
        except Exception as e:
            return {"error": str(e)}
        if response.ok:
            response = response.json()
            if response["error"] != "" and response["status"] < 400:
                return {"error": response["error"]}
            return {
                "url": f"https://spaceb.in/{response['payload']['id']}",
                "raw": f"{siteurl}{response['payload']['id']}/raw",
                "bin": "Spacebin",
            }
        return {"error": "Unable to reach spacebin."}


    def spaste(self: "pyAyiin.pyAyiin", message, extension="txt"):
        siteurl = "https://spaceb.in/api/v1/documents/"
        try:
            response = requests.post(
                siteurl, data={"content": message, "extension": extension}
            )
        except Exception as e:
            return {"error": str(e)}
        if response.ok:
            response = response.json()
            if response["error"] != "" and response["status"] < 400:
                return {"error": response["error"]}
            return {
                "url": f"https://spaceb.in/{response['payload']['id']}",
                "raw": f"{siteurl}{response['payload']['id']}/raw",
                "bin": "Spacebin",
            }
        return {"error": "Unable to reach spacebin."}


    async def n_paste(self: "pyAyiin.pyAyiin", message, extension=None):
        siteurl = "https://nekobin.com/api/documents"
        data = {"content": message}
        try:
            response = requests.post(
                url=siteurl,
                data=json.dumps(data),
                headers=headers)
        except Exception as e:
            return {"error": str(e)}
        if response.ok:
            response = response.json()
            purl = (
                f"nekobin.com/{response['result']['key']}.{extension}"
                if extension
                else f"nekobin.com/{response['result']['key']}"
            )
            return {
                "url": purl,
                "raw": f"nekobin.com/raw/{response['result']['key']}",
                "bin": "Neko",
            }
        return {"error": "Unable to reach nekobin."}


    async def d_paste(self: "pyAyiin.pyAyiin", message, extension=None):
        siteurl = "http://catbin.up.railway.app/documents"
        data = {"content": message}
        try:
            response = requests.post(
                url=siteurl,
                data=json.dumps(data),
                headers=headers)
        except Exception as e:
            return {"error": str(e)}
        if response.ok:
            response = response.json()
            purl = (
                f"http://catbin.up.railway.app/{response['key']}.{extension}"
                if extension
                else f"http://catbin.up.railway.app/{response['key']}"
            )
            return {
                "url": purl,
                "raw": f"http://catbin.up.railway.app/raw/{response['key']}",
                "bin": "Dog",
            }
        return {"error": "Unable to reach dogbin."}


    async def pastetext(self: "pyAyiin.pyAyiin", text_to_print, pastetype=None, extension=None):
        response = {"error": "something went wrong"}
        if pastetype is not None:
            if pastetype == "p":
                response = await self.p_paste(text_to_print, extension)
            elif pastetype == "s" and extension:
                response = await self.s_paste(text_to_print, extension)
            elif pastetype == "s":
                response = await self.s_paste(text_to_print)
            elif pastetype == "d":
                response = await self.d_paste(text_to_print, extension)
            elif pastetype == "n":
                response = await self.n_paste(text_to_print, extension)
        if "error" in response:
            response = await self.p_paste(text_to_print, extension)
        if "error" in response:
            response = await self.n_paste(text_to_print, extension)
        if "error" in response:
            if extension:
                response = await self.s_paste(text_to_print, extension)
            else:
                response = await self.s_paste(text_to_print)
        if "error" in response:
            response = await self.d_paste(text_to_print, extension)
        return response
