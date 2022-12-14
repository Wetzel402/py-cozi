#!/usr/bin/env python
import json
import aiohttp
import logging

from .exceptions import CoziException, InvalidLoginException, RequestException, REQUEST

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

# urls
URL_BASE = "https://rest.cozi.com"
URL_LOGIN = "{}/api/ext/2207/auth/login".format(URL_BASE)
URL_PERSON = "{}/api/ext/2004/{}/account/person/"
URL_LISTS = "{}/api/ext/2004/{}/list/"
URL_LIST = "{}/api/ext/2004/{}/list/{}"
URL_ITEMS = "{}/api/ext/2004/{}/list/{}/item/"
URL_ITEM = "{}/api/ext/2004/{}/list/{}/item/{}"
URL_CALENDAR = "{}/api/ext/2004/{}/calendar/{}/{}"

# response
RES_TOKEN_EXPIRES = "expiresIn"
RES_ACCESS_TOKEN = "accessToken"
RES_ACCT_ID = "accountId"

# form fields when logging in
FORM_KEY_USERNAME = "username"
FORM_KEY_PASSWORD = "password"
FORM_KEY_OPTION = "issueRefresh"


class Cozi:
    def __init__(self, username, password):
        """Set Cozi username and password."""
        self._username = username
        self._password = password
        self._token_expires = None
        self._access_token = None
        self._acct_id = None
        self._headers = {}

    # log into Cozi
    async def login(self):
        """login the user"""
        session = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar())
        async with session.post(
            URL_LOGIN,
            json={
                FORM_KEY_USERNAME: self._username,
                FORM_KEY_PASSWORD: self._password,
                FORM_KEY_OPTION: True,
            },
        ) as resp:
            _json_resp = await resp.json()
            if resp.status == 200:
                for key, value in _json_resp.items():
                    if key == RES_TOKEN_EXPIRES:
                        self._token_expires = value
                        LOGGER.debug(
                            "cozi found _token_expires {}".format(self._token_expires)
                        )
                    if key == RES_ACCESS_TOKEN:
                        self._access_token = value
                        self._headers["Authorization"] = "Bearer " + value
                        LOGGER.debug(
                            "cozi found _access_token {}".format(self._access_token)
                        )
                    if key == RES_ACCT_ID:
                        self._acct_id = value
                        LOGGER.debug("cozi found _acct_id {}".format(self._acct_id))
                LOGGER.info("cozi logged in")
            else:
                LOGGER.error("Error: could not log in..." + str(resp.status))
                LOGGER.error(_json_resp)
                raise InvalidLoginException("Error: could not log in")

        await session.close()

    async def get_persons(self, is_retry=False):
        """get persons"""
        if not self._access_token:
            await self.login()

        try:
            session = aiohttp.ClientSession(headers=self._headers)
            async with session.get(URL_PERSON.format(URL_BASE, self._acct_id)) as resp:
                _json_resp = await resp.json()
                await session.close()
                if resp.status < 400:
                    LOGGER.debug(_json_resp)
                    return _json_resp
        except RequestException:
            LOGGER.info("Cozi connection reset...")

        if not is_retry:
            # Delete our current token and try again -- will force a login attempt.
            self._access_token = None

            return self.get_persons(True)

        raise CoziException((REQUEST, _json_resp))

    # list functions
    async def get_lists(self, is_retry=False):
        """get all lists"""
        if not self._access_token:
            await self.login()

        try:
            session = aiohttp.ClientSession(headers=self._headers)
            async with session.get(URL_LISTS.format(URL_BASE, self._acct_id)) as resp:
                _json_resp = await resp.json()
                await session.close()
                if resp.status < 400:
                    LOGGER.debug(_json_resp)
                    return _json_resp
        except RequestException:
            LOGGER.info("Cozi connection reset...")

        if not is_retry:
            # Delete our current token and try again -- will force a login attempt.
            self._access_token = None

            return self.get_persons(True)

        raise CoziException((REQUEST, _json_resp))

    async def add_list(self, list_title, list_type, is_retry=False):
        """adds a new list"""
        if not self._access_token:
            await self.login()

        try:
            session = aiohttp.ClientSession(headers=self._headers)
            async with session.post(
                URL_LISTS.format(URL_BASE, self._acct_id),
                json={"title": list_title, "listType": list_type},
            ) as resp:
                LOGGER.debug("HTTP status code: " + str(resp.status))
                _json_resp = await resp.json()
                await session.close()
                if resp.status < 400:
                    LOGGER.debug(_json_resp)
                    return _json_resp
        except RequestException:
            LOGGER.info("Cozi connection reset...")

        if not is_retry:
            # Delete our current token and try again -- will force a login attempt.
            self._access_token = None

            return self.get_persons(True)

        raise CoziException((REQUEST, _json_resp))

    async def remove_list(self, list_id, is_retry=False):
        """removes a list"""
        if not self._access_token:
            await self.login()

        try:
            session = aiohttp.ClientSession(headers=self._headers)
            async with session.delete(
                URL_LIST.format(URL_BASE, self._acct_id, list_id)
            ) as resp:
                _json_resp = await resp.json()
                await session.close()
                if resp.status < 400:
                    LOGGER.debug(_json_resp)
                    return _json_resp
        except RequestException:
            LOGGER.info("Cozi connection reset...")

        if not is_retry:
            # Delete our current token and try again -- will force a login attempt.
            self._access_token = None

            return self.get_persons(True)

        raise CoziException((REQUEST, _json_resp))

    async def reorder_list(self, list_id, list_title, items, list_type):
        """reorders the items in a list"""
        if not self._access_token:
            await self.login()

        try:
            _data = {
                "externalIds": [],
                "title": list_title,
                "items": items,
                "notes": None,
                "listId": list_id,
                "version": None,
                "owner": None,
                "listType": list_type,
            }
            session = aiohttp.ClientSession(headers=self._headers)
            async with session.put(
                URL_LIST.format(URL_BASE, self._acct_id, list_id), json=_data
            ) as resp:
                _json_resp = await resp.json()
                await session.close()
                if resp.status < 400:
                    LOGGER.debug(_json_resp)
                    return _json_resp
        except RequestException:
            LOGGER.info("Cozi connection reset...")

        if not is_retry:
            # Delete our current token and try again -- will force a login attempt.
            self._access_token = None

            return self.get_persons(True)

        raise CoziException((REQUEST, _json_resp))

    # item functions
    async def add_item(self, list_id, item_text, item_pos, is_retry=False):
        """adds an item to a list"""
        if not self._access_token:
            await self.login()

        try:
            session = aiohttp.ClientSession(headers=self._headers)
            async with session.post(
                URL_ITEMS.format(URL_BASE, self._acct_id, list_id),
                json={"text": item_text, "position": item_pos},
            ) as resp:
                _json_resp = await resp.json()
                await session.close()
                if resp.status < 400:
                    LOGGER.debug(_json_resp)
                    return _json_resp
        except RequestException:
            LOGGER.info("Cozi connection reset...")

        if not is_retry:
            # Delete our current token and try again -- will force a login attempt.
            self._access_token = None

            return self.get_persons(True)

        raise CoziException((REQUEST, _json_resp))

    async def edit_item(self, list_id, item_id, item_text, is_retry=False):
        """edits an item in a list"""
        if not self._access_token:
            await self.login()

        try:
            session = aiohttp.ClientSession(headers=self._headers)
            async with session.put(
                URL_ITEM.format(URL_BASE, self._acct_id, list_id, item_id),
                json={"text": item_text},
            ) as resp:
                _json_resp = await resp.json()
                await session.close()
                if resp.status < 400:
                    LOGGER.debug(_json_resp)
                    return _json_resp
        except RequestException:
            LOGGER.info("Cozi connection reset...")

        if not is_retry:
            # Delete our current token and try again -- will force a login attempt.
            self._access_token = None

            return self.get_persons(True)

        raise CoziException((REQUEST, _json_resp))

    async def mark_item(self, list_id, item_id, status, is_retry=False):
        """marks an item complete or incomplete"""
        if not self._access_token:
            await self.login()

        try:
            session = aiohttp.ClientSession(headers=self._headers)
            async with session.put(
                URL_ITEM.format(URL_BASE, self._acct_id, list_id, item_id),
                json={"status": status},
            ) as resp:
                _json_resp = await resp.json()
                await session.close()
                if resp.status < 400:
                    LOGGER.debug(_json_resp)
                    return _json_resp
        except RequestException:
            LOGGER.info("Cozi connection reset...")

        if not is_retry:
            # Delete our current token and try again -- will force a login attempt.
            self._access_token = None

            return self.get_persons(True)

        raise CoziException((REQUEST, _json_resp))

    async def remove_items(self, list_id, items, is_retry=False):
        """removes items from the list weather marked complete or not"""
        """this is just how Cozi handles removing items so be careful"""
        if not self._access_token:
            await self.login()

        try:
            _data = {
                "operations": [{"op": "remove", "path": "/items/" + i} for i in items]
            }
            session = aiohttp.ClientSession(headers=self._headers)
            async with session.patch(
                URL_LIST.format(URL_BASE, self._acct_id, list_id), json=_data
            ) as resp:
                _json_resp = await resp.json()
                await session.close()
                if resp.status < 400:
                    LOGGER.debug(_json_resp)
                    return _json_resp
        except RequestException:
            LOGGER.info("Cozi connection reset...")

        if not is_retry:
            # Delete our current token and try again -- will force a login attempt.
            self._access_token = None

            return self.get_persons(True)

        raise CoziException((REQUEST, _json_resp))

    # calendar functions
    async def get_calendar(self, year, month, is_retry=False):
        """get calendar appointments"""
        if not self._access_token:
            await self.login()

        try:
            session = aiohttp.ClientSession(headers=self._headers)
            async with session.get(
                URL_CALENDAR.format(URL_BASE, self._acct_id, year, month)
            ) as resp:
                _json_resp = await resp.json()
                await session.close()
                if resp.status < 400:
                    LOGGER.debug(_json_resp)
                    return _json_resp
        except RequestException:
            LOGGER.info("Cozi connection reset...")

        if not is_retry:
            # Delete our current token and try again -- will force a login attempt.
            self._access_token = None

            return self.get_persons(True)

        raise CoziException((REQUEST, _json_resp))

    # appointment functions
    async def add_appointment(
        self,
        year,
        month,
        day,
        _start_time,
        end_time,
        date_span,
        attendees,
        location,
        notes,
        subject,
        is_retry=False,
    ):
        """add calendar appointment"""
        if not self._access_token:
            await self.login()

        try:
            if len(str(month)) < 2:
                _temp_month = "0" + str(month)
            else:
                _temp_month = str(month)

            if len(str(day)) < 2:
                _temp_day = "0" + str(day)
            else:
                _temp_day = str(day)

            _data = [
                {
                    "itemType": "appointment",
                    "create": {
                        "startDay": str(year) + "-" + _temp_month + "-" + _temp_day,
                        "details": {
                            "startTime": _start_time,
                            "endTime": end_time,
                            "dateSpan": date_span,
                            "attendeeSet": [attendees],
                            "location": location,
                            "notes": notes,
                            "subject": subject,
                        },
                    },
                }
            ]
            session = aiohttp.ClientSession(headers=self._headers)
            async with session.post(
                URL_CALENDAR.format(URL_BASE, self._acct_id, year, month), json=_data
            ) as resp:
                _json_resp = await resp.json()
                await session.close()
                if resp.status < 400:
                    LOGGER.debug(_json_resp)
                    return _json_resp
        except RequestException:
            LOGGER.info("Cozi connection reset...")

        if not is_retry:
            # Delete our current token and try again -- will force a login attempt.
            self._access_token = None

            return self.get_persons(True)

        raise CoziException((REQUEST, _json_resp))

    async def edit_appointment(
        self,
        appt_id,
        year,
        month,
        day,
        start_time,
        end_time,
        date_span,
        attendees,
        subject,
        is_retry=False,
    ):
        """edit calendar appointment"""
        if not self._access_token:
            await self.login()

        try:
            if len(str(month)) < 2:
                _temp_month = "0" + str(month)
            else:
                _temp_month = str(month)

            if len(str(day)) < 2:
                _temp_day = "0" + str(day)
            else:
                _temp_day = str(day)

            _data = [
                {
                    "itemType": "appointment",
                    "edit": {
                        "id": appt_id,
                        "startDay": str(year) + "-" + _temp_month + "-" + _temp_day,
                        "details": {
                            "startTime": start_time,
                            "endTime": end_time,
                            "dateSpan": date_span,
                            "attendeeSet": [attendees],
                            "subject": _subject,
                        },
                    },
                }
            ]
            session = aiohttp.ClientSession(headers=self._headers)
            async with session.post(
                URL_CALENDAR.format(URL_BASE, self._acct_id, year, month), json=_data
            ) as resp:
                _json_resp = await resp.json()
                await session.close()
                if resp.status < 400:
                    LOGGER.debug(_json_resp)
                    return _json_resp
        except RequestException:
            LOGGER.info("Cozi connection reset...")

        if not is_retry:
            # Delete our current token and try again -- will force a login attempt.
            self._access_token = None

            return self.get_persons(True)

        raise CoziException((REQUEST, _json_resp))

    async def remove_appointment(self, year, month, appt_id, is_retry=False):
        """removes a calendar appointment"""
        if not self._access_token:
            await self.login()

        try:
            _data = [{"itemType": "appointment", "delete": {"id": appt_id}}]
            session = aiohttp.ClientSession(headers=self._headers)
            async with session.post(
                URL_CALENDAR.format(URL_BASE, self._acct_id, year, month), json=_data
            ) as resp:
                _json_resp = await resp.json()
                await session.close()
                if resp.status < 400:
                    LOGGER.debug(_json_resp)
                    return _json_resp
        except RequestException:
            LOGGER.info("Cozi connection reset...")

        if not is_retry:
            # Delete our current token and try again -- will force a login attempt.
            self._access_token = None

            return self.get_persons(True)

        raise CoziException((REQUEST, _json_resp))
