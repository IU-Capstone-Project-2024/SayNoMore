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

| **Step No.** | **Message Sent**         | **Bot Response**                                             | **Code Crash Message (if any)**                              |
|--------------|--------------------------|--------------------------------------------------------------|--------------------------------------------------------------|
| 1            | Я хочу уехать из Казани  | *Ваш запрос не содержит некоторых необходимых данных. Пожалуйста, укажите даты вылета и возвращения, а также город назначения. Кроме того, если у вас есть бюджет, вы можете указать и его, хотя это не обязательно. Спасибо!* | *-*                                                          |
| 2            | 1 июля                   | *Ваш запрос не содержит информацию о городе отправления и назначения. Пожалуйста, укажите эти данные. Кроме того, если у вас есть бюджет, вы можете указать и его, хотя это не обязательно. Спасибо!* | *-*                                                          |
| 3            | в москву до 7 июля       |                                                              | <br> File "/home/SayNoMore/api_collector/route/route.py", line 332, in find_top_routes<br>    if cheapest_hotel['priceFrom'] + cheapest_ticket['price'] > budget:<br>TypeError: '>' not supported between instances of 'float' and 'str' |

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
