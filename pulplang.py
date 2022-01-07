import lex
import yacc

tokens = (
    'ARTISTS', 'TRACKS', 'ALBUMS', 'LIMIT', 
    'CREATE_PLAYLIST', 'UPDATE_PLAYLIST', 'NAME',
    'NUMBER', 'WHITESPACE', 'NEWLINE', 'ONLY_LIKED', 
    'MINUTES', 'END_SECTION'
)

def t_ARTISTS(t):
    r'[artists|ar][\s+|\n+]'
    return t

def t_TRACKS(t):
    r'[tracks|tr][\s+|\n+]'
    return t

def t_ALBUMS(t):
    r'[albums|al][\s+|\n+]'
    return t

def t_LIMIT(t):
    r'[limit|l]\s+'
    return t

def t_CREATE_PLAYLIST(t):
    r'[create playlist|cp][\s+|\n+]'
    return t

def t_UPDATE_PLAYLIST(t):
    r'[update playlist|up][\s+|\n+]'
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\s+\d+[\s+|\n+]'
    t.value = int(t.value)
    return t

def t_WHITESPACE(t):
    r'\s+'
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_ONLY_LIKED(t):
    r'\s+[only liked|ol][\s+|\n+]'
    return t

def t_MINUTES(t):
    r'\s+[min|m][\s+|\n]'
    return t

def t_END_SECTION(t):
    r'\s--\s'
    return t

lexer = lex.lex()

tokens = lexer.lextokens

def p_pulp(p):
    '''pulp : '''

def p_track(p):
    '''track : NAME'''
    p[0] = ('track_by_name', p[1])

def p_tracklist(p):
    '''tracklist : tracklist WHITESPACE track
                 | tracklist NEWLINE track
                 | track'''
    if len(p) > 2:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = [p[1]]

def p_tracks(p):
    '''tracks : TRACKS tracklist END_SECTION''' #need to terminate list at next reserved token word
    p[0] = p[2]

def p_artist(p):
    '''artist : NAME
              | NAME NUMBER'''
    if len(p) == 2:
        p[0] = ('artist_by_name', p[1])
    elif len(p) == 3:
        p[0] = ('artist_by_name_number', p[1], p[2])

def p_artistlist(p):
    '''artistlist : artistlist WHITESPACE artist
                  | artistlist NEWLINE artist
                  | artist'''
    if len(p) > 2:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = [p[1]]

def p_artists(p):
    '''artists : ARTISTS artistlist END_SECTION'''
    p[0] = p[2]

def p_album(p):
    '''album : NAME
             | NAME ONLY_LIKED'''
    if len(p) == 2:
        p[0] = ('album_by_name', p[1])
    elif len(p) == 3:
        p[0] = ('album_by_name_onlyliked', p[1], p[2])

def p_albumlist(p):
    '''albumlist : albumlist WHITESPACE album
                  | albumlist NEWLINE album
                  | album'''
    if len(p) > 2:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = [p[1]]

def p_albums(p):
    '''albums : ALBUMS albumlist END_SECTION'''
    p[0] = p[2]

def p_limitbyminutes(p):
    '''limit : NUMBER MINUTES'''
    p[0] = ('limit_by_minutes', p[1])

def p_limitbynumtracks(p):
    '''limit : NUMBER TRACKS'''
    p[0] = ('limit_by_numtracks', p[1])




yacc.yacc()


