from music.utils.menu import main_menu


def get_music_context(request):
    return {'mainmenu': main_menu}