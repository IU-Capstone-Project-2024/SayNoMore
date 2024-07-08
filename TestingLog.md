### Telegram Bot User Interaction Testing Log

#### **Test Case ID**: TC001  
**Date**: 2024-06-26  
**Tester**: Maxim Martyshov  
**Scenario**: Normal interaction  

---

#### **Test Case Description:**
This test performs a standard sequence of messages, all of which provide ideal information without typos, enabling the bot to construct a route effectively.

---

#### **Test Log:**

| **Step No.** | **Message Sent**                                             | **Bot Response**                                             | **Code Crash Message (if any)** |
|--------------|--------------------------------------------------------------|--------------------------------------------------------------|---------------------------------|
| 1            | `/start`                                                     | *Hi, welcome to SayNoMore bot. Tell us more about the trip you are planning.* | *-*                             |
| 2            | Я хочу съездить в Москву из Казани с 1e по 7e июля, с бюджетом в 100 тысяч рублей | *Route from KZN to MOW:<br>Flight: KZN to MOW, Departing at: 2024-07-07T11:20:00+03:00, Returning at: 2024-07-07T22:55:00+03:00, Airline: N4, Flight Number: 246, Price: 40427 rub, Transfers: 1, Return Transfers: 1, Duration: 920 minutes<br>Hotel: Apartament, Location: Moscow, None, Russia, Stars: 0, Price From: 10411.88 rub, Average Price: 10411.88 rub* | *-*                             |

---

#### **Additional Notes:**
- The bot works with various date formats (7, 7th, seventh).

---

#### **Test Case ID**: TC002  
**Date**: 2024-06-26  
**Tester**: Maxim Martyshov  
**Scenario**: Gradually feeding the information about the trip  

---

#### **Test Case Description:**
This test feeds the bot information about the trip step by step. The goal is to make the bot ask for additional information until it is satisfied, with clear inputs free from errors and typos.

---

#### **Test Log:**

| **Step No.** | **Message Sent**        | **Bot Response**                                             | **Code Crash Message (if any)**                              |
|--------------|-------------------------|--------------------------------------------------------------|--------------------------------------------------------------|
| 1            | Я хочу уехать из Казани | *Ваш запрос не содержит некоторых необходимых данных. Пожалуйста, укажите даты вылета и возвращения, а также город назначения. Кроме того, если у вас есть бюджет, вы можете указать и его, хотя это не обязательно. Спасибо!* | *-*                                                          |
| 2            | 1 июля                  | *Ваш запрос не содержит информацию о городе отправления и назначения. Пожалуйста, укажите эти данные. Кроме того, если у вас есть бюджет, вы можете указать и его, хотя это не обязательно. Спасибо!* | *-*                                                          |
| 3            | в москву до 7 июля      |                                                              |   File "/home/SayNoMore/api_collector/route/route.py", line 332, in find_top_routes<br>    if cheapest_hotel['priceFrom'] + cheapest_ticket['price'] > budget:<br>TypeError: '>' not supported between instances of 'float' and 'str' |

---

#### **Additional Notes:**
- The program crashed because we do not ask the user to enter their budget. `Request analyzer` returns:
  ```json
  {"Arrival": "2024-07-01", "Return": "2024-07-01", "Departure": "KZN", "Destination": "MOW", "Budget": "None"}
  ```
  However, `find_top_routes` does not account for this, resulting in a crash.

---

#### **Test Case ID**: TC003  
**Date**: 2024-06-26  
**Tester**: Maxim Martyshov  
**Scenario**: Request with typos  

---

#### **Test Case Description:**
This test involves making a request with typos in crucial words like departure/destination city or a date, and trying different notations for the budget.

---

#### **Test Log:**

| **Step No.** | **Message Sent**                            | **Bot Response**                                             | **Code Crash Message (if any)**                              |
|--------------|---------------------------------------------|--------------------------------------------------------------|--------------------------------------------------------------|
| 1            | Я хочу уехать из Кзн 1 июля                 | *Ваш запрос не содержит некоторых необходимых данных. Пожалуйста, укажите даты вылета и возвращения, а также город назначения. Кроме того, если у вас есть бюджет, вы можете указать и его, хотя это не обязательно. Спасибо!* | *-*                                                          |
| 2            | в мскву до седьмого июля, бюджет: 100тыс. ₽ |                                                              | <br>File "/home/SayNoMore/api_collector/air_tickets/air_tickets_api.py", line 101, in fetch_cheapest_tickets<br>    raise Exception(<br>Exception: Failed to fetch cheapest tickets. Status code: 400 |

---

#### **Additional Notes:**
- Here is the `Request analyzer` return from this interaction:
  ```json
  {"Arrival": "2024-07-01", "Return": "2024-07-01", "Departure": "Кзн", "Destination": "MOW", "Budget": 100000}
  ```
  We see an issue with the return date; it did not understand the alphabetical notation of the date. Additionally, it cannot handle city abbreviations like 'КЗН' which stands for Kazan.
- We also ran the test with:
  > "бюджет: 100 т.р."
  - This works fine.

---

#### **Test Case ID**: TC004  
**Date**: 2024-07-01
**Tester**: Maxim Martyshov  
**Scenario**: Request with error

---

#### **Test Case Description:**
This test involves making a request with an error in it. Specifically, what if a user provides a departure or arrival date that is in the past?

---

#### **Test Log:**

| **Step No.** | **Message Sent**                | **Bot Response**                                             | **Code Crash Message (if any)** |
|--------------|---------------------------------|--------------------------------------------------------------|---------------------------------|
| 1            | хочу уехать из Казани 1 июня    | *Ваш запрос не содержит некоторых необходимых данных. Пожалуйста, укажите даты вылета и возвращения, а также город назначения. Кроме того, если у вас есть бюджет, вы можете указать и его, хотя это не обязательно. Спасибо!* | *-*                             |
| 2            | в москву до 7 июня              | Ваш запрос содержит некоторые ошибки. Пожалуйста, убедитесь, что дата возвращения введена позднее даты прибытия. Кроме того, если у вас есть бюджет, вы можете указать и его, хотя это не обязательно. Спасибо! | *-*                             |
| 3            | в москву до 7 июля бюджет 100тр | *Route from KZN to MOW:<br>Flight: KZN to MOW, Departing at: 2024-07-07T07:55:00+03:00, Returning at: 2024-07-07T20:40:00+03:00, Airline: N4, Flight Number: 250, Price: 43946 rub, Transfers: 1, Return Transfers: 1, Duration: 955 minutes<br>Hotel: 1-комнатная квартира, Location: Moscow, None, Russia, Stars: 0, Price From: 8551.76 rub, Average Price: 8551.76 rub* | *-*                             |

---

#### **Additional Notes:**
- Here is the `Request analyzer` return from this interaction:
  ```json
  {"Arrival": "2024-07-07", "Return": "2024-07-07", "Departure": "KZN", "Destination": "MOW", "Budget": 100000}
  ```
  We see some issues with arrival retrieval.

---

#### **Test Case ID**: TC005  
**Date**: 2024-07-02
**Tester**: Maxim Martyshov  
**Scenario**: Request outside Russia 

---

#### **Test Case Description:**
This test involves making a request that will be completely outside the Russian Federation. I will ask for a trip plan from London to Paris.

---

#### **Test Log:**

| **Step No.** | **Message Sent**                                          | **Bot Response** | **Code Crash Message (if any)**                              |
|--------------|-----------------------------------------------------------|------------------|--------------------------------------------------------------|
| 1            | Хочу уехать из Лондона в Париж с 3 по 9 июля бюджет 300тр |                  | *File "/home/SayNoMore/api_collector/air_tickets/air_tickets_api.py", line 101, in fetch_cheapest_tickets<br>    raise Exception(<br>Exception: Failed to fetch cheapest tickets. Status code: 420* |

---

#### **Additional Notes:**
- Here is the `Request analyzer` return from this interaction:
  ```json
  {"Arrival": "2024-07-09", "Return": "2024-07-09", "Departure": "LOZ", "Destination": "PRX", "Budget": 300000}
  ```
  * We notice some issues with the arrival retrieval.
  * `LOZ` is the IATA code for London-Corbin Airport in the USA, and we need `LHR` for London Heathrow.
  * `PRX` IATA code is also incorrect. Paris is `CDG`.

---

#### **Test Case ID**: TC006  
**Date**: 2024-07-02
**Tester**: Maxim Martyshov  
**Scenario**: Request outside Russia 2

---

#### **Test Case Description:**
This test involves making a request that will build a route from Russia to outside of Russia and will be a direct flight.

---

#### **Test Log:**

| **Step No.** | **Message Sent**                                             | **Bot Response**                                             | **Code Crash Message (if any)** |
|--------------|--------------------------------------------------------------|--------------------------------------------------------------|---------------------------------|
| 1            | Хочу уехать из Москвы 4 июля в Белград до 9го июля бюджет 400 тр | *Route from MOW to BEG:<br>Flight: MOW to BEG, Departing at: 2024-07-04T00:55:00+03:00, Returning at: 2024-07-04T20:20:00+02:00, Airline: TK, Flight Number: 412, Price: 341374 rub, Transfers: 2, Return Transfers: 1, Duration: 1260 minutes<br>Hotel: HostGost at Molerova 9, Location: Belgrade, None, Serbia, Stars: 0, Price From: 8392.59 rub, Average Price: 8392.59 rub* | *-*                             |

---

#### **Additional Notes:**
- Here is the `Request analyzer` return from this interaction:
  ```json
  {"Arrival": "2024-07-04", "Return": "2024-07-04", "Departure": "MOW", "Destination": "BEG", "Budget": 400000}
  ```
  * We notice some issues with the arrival retrieval.

---

#### **Test Case ID**: TC007  
**Date**: 2024-07-02
**Tester**: Maxim Martyshov  
**Scenario**: Request outside Russia 3

---

#### **Test Case Description:**
This test involves making a request that will build a route from Russia to outside of Russia and will be a flight with a connection.

---

#### **Test Log:**

| **Step No.** | **Message Sent**                                             | **Bot Response**                                             | **Code Crash Message (if any)** |
|--------------|--------------------------------------------------------------|--------------------------------------------------------------|---------------------------------|
| 1            | Хочу уехать из Москвы 4 июля в Рим до 9го июля бюджет 400 тр | *Route from MOW to ROM:<br>Flight: MOW to ROM, Departing at: 2024-07-09T08:15:00+03:00, Returning at: 2024-07-09T22:30:00+02:00, Airline: EK, Flight Number: 0130, Price: 258026 rub, Transfers: 1, Return Transfers: 1, Duration: 2065 minutes<br>Hotel: SM Vatican Relais, Location: Rome, None, Italy, Stars: 2, Price From: 30224.8 rub, Average Price: 30224.8 rub<br>________________________<br>Route from MOW to ROM:<br>Flight: MOW to ROM, Departing at: 2024-07-09T04:40:00+03:00, Returning at: 2024-07-09T22:10:00+02:00, Airline: FZ, Flight Number: 968, Price: 363997 rub, Transfers: 1, Return Transfers: 1, Duration: 1890 minutes<br>Hotel: Hotel Lord Byron - Small Luxury Hotels of the World, Location: Rome, None, Italy, Stars: 5, Price From: 36135.16 rub, Average Price: 36135.16 rub<br>________________________* | *-*                             |

---

#### **Additional Notes:**
- Here is the `Request analyzer` return from this interaction:
  ```json
  {"Arrival": "2024-07-09", "Return": "2024-07-09", "Departure": "MOW", "Destination": "ROM", "Budget": 400000}
  ```
  * We notice some issues with the arrival retrieval.
  * Connections are not displayed.

---
#### **Test Case ID**: TC008  
**Date**: 2024-07-08  
**Tester**: Maxim Martyshov  
**Scenario**: Request Reset Command

---

#### **Test Case Description:**
This test involves making a request and then hitting the reset button.

---

#### **Test Log:**

| **Step No.** | **Message Sent**        | **Bot Response**                                                                                   | **Code Crash Message (if any)**                              |
|--------------|-------------------------|----------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| 1            | Я хочу уехать из Казани | *Ваш запрос содержит некоторые пропущенные поля. Пожалуйста, укажите даты прибытия и возвращения, а также город назначения. Если у вас есть бюджет, вы можете указать его, хотя это не обязательно. Спасибо!* | *-*                                                          |
| 2            | /restart                | *-*                                                                                                | File "/home/SayNoMore/telegram_bot/telegram_bot.py", line 49, in restart_trip_planning<br>    language = user_states[user_id]["language"]<br>KeyError: 925371113 |

---

#### **Additional Notes:**
- The result of the test is that the restart command is completely non-functional.

___

#### **Test Case ID**: TC009  
**Date**: 2024-07-08  
**Tester**: Maxim Martyshov  
**Scenario**: Change Language

---

#### **Test Case Description:**
This test involves changing the language from the start of the conversation (not involving changing the language in the middle of the request).

---

#### **Test Log:**

| **Step No.** | **Message Sent**                                             | **Bot Response**                                             | **Code Crash Message (if any)** |
|--------------|--------------------------------------------------------------|--------------------------------------------------------------|---------------------------------|
| 1            | /start                                                       | Привет, добро пожаловать в бота SayNoMore. Расскажите нам больше о вашем планируемом путешествии. | *-*                             |
| 2            | /language                                                    | Choose your language / Выберите язык: <br><Русский><br><English><br><br>Language preference updated. | -                               |
| 3            | I wanna go to Moscow from Saint Petersburg from 12th July to 14th July | [Recommendation]                                              | -                               |

---

#### **Additional Notes:**
- In this scenario, everything works fine.

___

#### **Test Case ID**: TC010  
**Date**: 2024-07-08  
**Tester**: Maxim Martyshov  
**Scenario**: Change Language in the Middle of the Request

---

#### **Test Case Description:**
This test involves changing the language in the middle of the request.

---

#### **Test Log:**

| **Step No.** | **Message Sent**                   | **Bot Response**                                             | **Code Crash Message (if any)** |
|--------------|------------------------------------|--------------------------------------------------------------|---------------------------------|
| 1            | Я хочу уехать из Казани            | Ваш запрос содержит некоторые пропущенные поля. Пожалуйста, укажите даты прибытия и возвращения, а также город назначения. Если у вас есть бюджет, вы можете указать его, хотя это не обязательно. Спасибо! | *-*                             |
| 2            | /language                          | Choose your language / Выберите язык: <br><Русский><br><English><br><br>Language preference updated. | -                               |
| 3            | 12th July till 14th July to Moscow | [Recommendation]                                              | -                               |

---

#### **Additional Notes:**
- In this scenario, everything works fine.

___

#### **Test Case ID**: TC011  
**Date**: 2024-07-08  
**Tester**: Maxim Martyshov  
**Scenario**: Strange Behavior

---

#### **Test Case Description:**
This test involves typing some random text in the middle of the request.

---

#### **Test Log:**

| **Step No.** | **Message Sent**                         | **Bot Response**                                                                                   | **Code Crash Message (if any)** |
|--------------|------------------------------------------|----------------------------------------------------------------------------------------------------|---------------------------------|
| 1            | Я хочу уехать из Казани                  | Ваш запрос содержит некоторые пропущенные поля. Пожалуйста, укажите даты прибытия и возвращения, а также город назначения. Если у вас есть бюджет, вы можете указать его, хотя это не обязательно. Спасибо! | *-*                             |
| 2            | eijfbviebrib3urb                         | Ваш запрос не содержит необходимых данных. Пожалуйста, укажите даты прибытия и возвращения, а также город отправления и назначения. Если у вас есть бюджет, вы можете указать его, хотя это не обязательно. Спасибо! | -                               |
| 3            | вушпоимушмик                             | Ваш запрос не содержит необходимой информации. Пожалуйста, укажите даты поездки, город отправления, город назначения и бюджет, если он у вас есть. Спасибо! | -                               |
| 4            | 12го июля в Санкт-Петербург до 14го июля | [Recommendation]                                                                                   | -                               |

---

#### **Additional Notes:**
- In this scenario, everything works fine for both languages, Russian and English.

___
