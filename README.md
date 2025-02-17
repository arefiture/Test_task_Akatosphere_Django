# Test_task_Akatosphere_Django
Тестовое задание Акатосфера Django

# ТЗ
Реализовать API проекта магазина продуктов, используя Django Rest Framework, со следующим функционалом:
* <input type="checkbox" disabled> Должна быть реализована возможность создания, редактирования, удаления категорий и подкатегорий товаров в админке.
* <input type="checkbox" checked disabled> Категории и подкатегории обязательно должны иметь наименование, slug-имя, изображение
* <input type="checkbox" checked disabled> Подкатегории должны быть связаны с родительской категорией
* <input type="checkbox" disabled> Должен быть реализован эндпоинт для просмотра всех категорий с подкатегориями. Должны быть предусмотрена пагинация.
* <input type="checkbox" disabled> Должна быть реализована возможность добавления, изменения, удаления продуктов в админке.
* <input type="checkbox" checked disabled> Продукты должны относится к определенной подкатегории и, соответственно категории, должны иметь наименование, slug-имя, изображение в 3-х размерах, цену
* <input type="checkbox" disabled> Должен быть реализован эндпоинт вывода продуктов с пагинацией. Каждый продукт в выводе должен иметь поля: наименование, slug, категория, подкатегория, цена, список изображений
* <input type="checkbox" disabled> Реализовать эндпоинт добавления, изменения (изменение количества), удаления продукта в корзине.
* <input type="checkbox" disabled> Реализовать эндпоинт вывода  состава корзины с подсчетом количества товаров и суммы стоимости товаров в корзине.
* <input type="checkbox" disabled> Реализовать возможность полной очистки корзины
* <input type="checkbox" disabled> Операции по эндпоинтам категорий и продуктов может осуществлять любой пользователь
* <input type="checkbox" disabled> Операции по эндпоинтам корзины может осуществлять только авторизированный пользователь и только со своей корзиной
* <input type="checkbox" disabled> Реализовать авторизацию по токену
* <input type="checkbox" disabled> Реализовать фикстуры приложения
* <input type="checkbox" disabled> Подключить swagger и прислать ссылку.
* <input type="checkbox" disabled> Покрыть автотестами пару методов  GET и POST
* <input type="checkbox" disabled> Оформить README файл с описанием функционала приложения и инструкции по запуску приложения локально
