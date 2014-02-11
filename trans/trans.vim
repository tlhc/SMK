"the trans function by TL
function! TransL(word)
python << EOF

#coding=utf-8
import vim, urllib2, sys


def tras(word):
    s="trans-container"
    err="error-wrapper"

    request="http://dict.youdao.com/search?q=" + word + "&keyfrom=dict.index"

    url = urllib2.urlopen(request)
    d = url.read()

    epos = d.find(err.decode("utf-8").encode("utf-8"))

    if epos != -1:
        print "can't find "
        return
    else:
        print "translate....."

    pos = d.find(s.decode("utf-8").encode("utf-8"))
    ret = d[pos:pos + 5000]

    pos = ret.find("<ul>")
    pos1 = ret.find("</ul>")

    ret = ret[pos + 4:pos1]

    #print ret

    ret = ret.replace('<li>', '')
    ret = ret.replace('</li>', '')

    print ret
    return

word=vim.eval("a:word")
tras(word)
EOF
endfunction

function! GetWD() 
    let s:word = expand('<cword>')
    call TransL(s:word)
endfunction

nmap <C-T> : call GetWD() <CR>

