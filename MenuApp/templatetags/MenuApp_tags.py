from django import template
from MenuApp.models import *

register = template.Library()

@register.inclusion_tag('MenuApp/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name=None):
    if menu_name is None:
        return{
            'error': True,
            'error_text': 'Ошибка. Передайте тегу "draw_menu" имя существующего мею.',
        }
    
    def get_elements_from_path(all_menu=None,
                               menu_path_list=None,
                               elements_in_path=None):
        
        check_slug = '/'.join(menu_path_list)+'/'
        for element in all_menu:
            if element.slug == check_slug:
                elements_in_path.append(element)

                if len(menu_path_list) == 1:
                    return(elements_in_path[::-1])
                
                return(get_elements_from_path(all_menu=all_menu,
                                              menu_path_list=menu_path_list[0:-1],
                                              elements_in_path=elements_in_path))
               

    def get_menu(menu_first_element=None,
                 all_menu=None,
                 menu=None,
                 elements_in_path=None,
                 depth=None):

        for element in all_menu:
            if element.parent == menu_first_element:
                element.depth = depth
            #пример, как воплотить визуальное отображение глубины вложенности элемента нутри
            #python кода. Но я считаю, что визульное оформление не должно быть внутри бэкэнда

            #чтобы проверить работу, можно просто убрать комментарий со следующей строки и 
            #убрать комментарий внутри mytag.html с отображения element.depth_to_draw
            #и закомментировать скрипт js

                #element.depth_to_draw = ('&emsp;'*depth)

                menu.append(element)
                if element in elements_in_path:
                    depth+=1
                    get_menu(menu_first_element=element,
                             all_menu=all_menu,
                             menu=menu,
                             elements_in_path=elements_in_path,
                             depth=depth)
                    depth-=1
        return(menu)
    
    def return_fist_element(all_menu=None):
        for element in all_menu:
            if not element.parent:
                element.depth = 0
                return{
                    'menu': [element]
                }

#начало работы тега
    all_menu = list(Menu.objects.select_related('parent').filter(menu_name = menu_name).order_by('name'))
    
    if not all_menu:
        return{
            'error': True,
            'error_text': 'Ошибка. Передайте тегу "draw_menu" имя существующего мею.',
        }
    
    menu_path_list = context.request.path.split('/')[1:-1]

#Если нет пути в url, то следут отобразить первый эелемент в меню
#детей первого элемента отображать не надо, так как он не является выбранным

    if not menu_path_list:
        return(return_fist_element(all_menu=all_menu))

    elements_in_path = get_elements_from_path(all_menu=all_menu,
                                              menu_path_list=menu_path_list,
                                              elements_in_path=[])
#Если путь url не соотвкттвует меню, то следут отобразить первый эелемент в меню
#детей первого элемента отображать не надо, так как он не является выбранным
    if not elements_in_path:
        return(return_fist_element(all_menu=all_menu))

    elements_in_path[0].depth = 0
    menu = [elements_in_path[0]]
    menu = get_menu(menu_first_element=elements_in_path[0], 
                    all_menu=all_menu, 
                    menu=menu,
                    elements_in_path=elements_in_path,
                    depth = 1)

    return {
        'menu': menu
    }




#Моя первая идея решения. Этот вариант работает, но он менее эффективен, чем итоговый вариант выше
#И так же этот вариант не сделан до конца, хотя основная логика реализована

# @register.inclusion_tag('MenuApp/draw_menu.html', takes_context=True)
# def draw_menu_second_solution(context, menu_name=None):
# #начало работы тега на 76 строке, до 76 строки определяются необходимые  функции
# #Проще всего отрисовать такое меню со знанием детей для каждого элемента отображаемого меню
#     def collect_children(menu_first_element=None, menu_last_element=None, all_menu=None, collected_children=None):
#         new_last_element  = None
#         for element in all_menu:
#             if element.parent == menu_last_element:

#                 children_list = collected_children.get(menu_last_element)
#                 if children_list:
#                     children_list.append(element)
#                     collected_children.update({menu_last_element: children_list})

#                 else:
#                     collected_children.update({menu_last_element: [element]})

#             #пояснения к этой строке ниже
#             if element == menu_last_element:
#                 new_last_element = element.parent
                
#         if menu_last_element == menu_first_element:
#             list_of_parents_with_children = []
#             for parent, children_list in collected_children.items():
#                 parent.children = children_list
#                 list_of_parents_with_children.append(parent)

#             return (list_of_parents_with_children[::-1])

#         # menu_last_element = menu_last_element.parent

#             # закоментированная строка выше обращается к базе данных при каждом вызове collect_children, начиная 
#             # со второго, поэтому menu_last_element.parent нужно брать из переменной all_menu, так как all_menu - это лист, в котором 
#             # уже записаны данные родителей благодаря select_related, а menu_last_element - объект модели, в котором со 2
#             # вызова collect_children не хранится данных о родителе.
        
#         menu_last_element = new_last_element
#         return collect_children(menu_first_element=menu_first_element, 
#                                 menu_last_element=menu_last_element, 
#                                 all_menu=all_menu, 
#                                 collected_children=collected_children)

#     def unwrap_menu(menu_wrapped=None, menu_finished=None):
#         if menu_wrapped is None:
#             return(menu_finished)
        
#         for element in menu_wrapped:
#             menu_finished.append(element)
#             try:
#                 unwrap_menu(menu_wrapped = element.children, menu_finished=menu_finished)

#             except AttributeError:
#                 pass
        
#         return (menu_finished)
# #эта функция сама по себе не возвращает меню, она его структурирует, как бы, "сворачивая меню послойно"
# #благодаря чему можно уже внутри функции unwrap_menu создать лист из элементов меню, который при выводе
# #будет крректно отображать струткуру требуемого древовидного меню
#     def get_menu(menu_wrapped=None):
#         if len(menu_wrapped)<=1:
#             menu_finished = []
#             return(unwrap_menu(menu_wrapped=menu_wrapped, menu_finished=menu_finished))

#         last_element = menu_wrapped.pop(-1)
#         index = menu_wrapped[-1].children.index(last_element)
#         menu_wrapped[-1].children[index] = last_element

#         return(get_menu(menu_wrapped=menu_wrapped))
# #начало работы тега
#     all_menu = list(Menu.objects.select_related('parent').filter(menu_name = menu_name).order_by('name'))
#     menu_path = context.request.path[1:]

#     menu_last_element = None
#     menu_first_element = None

#     for element in all_menu:

#         if element.slug == menu_path:
#             menu_last_element = element

#         if element.parent is None:
#             menu_first_element = element

#     #если меню не совпадает с url
#     if menu_last_element is None:
#         return {
#             'menu': [menu_first_element]
#         }

#     collected_children = dict()
#     menu_wrapped = collect_children(menu_first_element=menu_first_element, 
#                                 menu_last_element=menu_last_element, 
#                                 all_menu=all_menu, 
#                                 collected_children=collected_children)
    
#     menu = get_menu(menu_wrapped=menu_wrapped)
#     #если в меню есть только один элемент
#     if not menu:
#         menu = [menu_first_element]

#     return {
#         'menu': menu
#     }