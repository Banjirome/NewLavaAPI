# NewLavaAPI ducumentation
## Начало
`pip install NewLavaAPI`
Для использования библиотеки вам необходимо создать экземпеляр LavaAPI с указанием api_key и shop_id вашего магазина.
```
api_key = '****************************************'
shopid = "********-****-****-****-************"
api = NewLavaAPI(api_key, shopid)
```
При обьявлении этого класса происходит автоматическая проверка валидности указанных данных.
## Использование
В созданном вами экземпляре имеются следующие функции:
1. `create_invoice()` - Принимает в себя айди счета, сумму и комментарий к вашему чеку. Важно: айди счета существующих чеков должны быть уникальными
1. `balance()` - Возвращает баланс вашего магазина в валюте, указанной в личном кабинете

## Статусы платежей
Функция `create_invoice()` возвращает класс типа Payment(). Он содержит в себе информацию о выставленном счете (orderID, paymentID, payment_url)
В нем есть функцию проверки платежа `check_invoice_status()` возвращающая True или False в зависимости от статуса платежа

## Пример
```
import NewLavaAPI
import random

api_key = '****************************************'
shopid = "********-****-****-****-************"
api = NewLavaAPI(api_key, shopid) # Вызываем класс NewLavaAPI

print(f"Ваш баланс: {api.balance()}")
orderid = random.randint(11111111, 99999999) # Лучше всего генерировать orderID случайно
print(f"Создаем платеж с номером: {orderid}")
payment = api.create_invoice(orderid, float(amount), comment)
print(f"URL счета: {payment.url}")
print(f"Айди счета: {payment.paymentID}")
payment_status = payment.check_invoice_status()
if payment_status:
  print(f"Счет оплачен")
else:
  print(f"Счет не оплачен")

```
