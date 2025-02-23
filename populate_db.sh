#!/bin/bash

# URL-адреса API
BASE_URL="http://localhost:8000/api"

# Данные пользователя для регистрации/логина
FIRST_NAME="First"
LAST_NAME="User"
USERNAME="first_user_test"
EMAIL="test@example.com"
PASSWORD="TestU6er"

# 1. Регистрация пользователя
REG_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register/" \
  -H "Content-Type: application/json" \
  -d "{\"first_name\": \"$FIRST_NAME\", \"last_name\": \"$LAST_NAME\", \"email\": \"$EMAIL\", \"username\": \"$USERNAME\", \"password\": \"$PASSWORD\", \"confirm_password\": \"$PASSWORD\"}")

echo "Registration response: $REG_RESPONSE"

# 2. Достаём токены из ответа
ACCESS_TOKEN=$(echo "$REG_RESPONSE" | grep -o '"access":"[^"]*' | sed 's/"access":"//')
REFRESH_TOKEN=$(echo "$REG_RESPONSE" | grep -o '"refresh":"[^"]*' | sed 's/"refresh":"//')

echo "Access Token: $ACCESS_TOKEN"

# Проверяем, что токен получен
if [ "$ACCESS_TOKEN" == "null" ]; then
  echo "Ошибка авторизации"
  exit 1
fi

# 3. Добавляем предметы в корзину
ITEMS=("1:0.5" "3:0.7" "4:0.7" "5:1" "6:2" "9:3")

for ITEM in "${ITEMS[@]}"; do
  ITEM_ID=${ITEM%%:*}
  AMOUNT=${ITEM##*:}
  
  # Отправка запроса
  CART_RESPONSE=$(curl -s -X POST "$BASE_URL/product/$ITEM_ID/shop_action/" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"amount\": $AMOUNT}")

  echo "Добавлен товар $ITEM_ID (количество: $AMOUNT): $CART_RESPONSE"
done

echo "Тестовые данные успешно добавлены!"
