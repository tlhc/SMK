"the trans function by TL
function! <SID>TransL(word)
python << EOF

#coding=utf-8
import vim, urllib2, sys
def tras(word):
    s="trans-container"
    err="error-wrapper"

    request="http://dict.youdao.com/search?q=" + word + "&keyfrom=dict.index"

    try:
        url = urllib2.urlopen(request, None, 2)
        d = url.read()
    except:
        print "req time out"
        return

    epos = d.find(err.decode("utf-8").encode("utf-8"))

    if epos != -1:
        print "can't find "
        return
    else:
        print word + ":"

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

function! <SID>GetWD() 
   let s:word = expand('<cword>')
   call <SID>TransL(s:word)
endfunction

function! <SID>GetVWD()
    let s:word = <SID>GetVisualSelection()
    call <SID>TransL(s:word)
endfunction


function! <SID>GetVisualSelection()
    try
        let a_save = @a
        normal! gv"ay
        return @a
    finally
        let @a = a_save
    endtry
endfunction

command GetWD :call <SID>GetWD()
command GetVWD :call <SID>GetVWD()
"nmap <silent> <c-s-K> <Esc>: call GetWD() <CR>
"vmap <silent> <c-s-K> <Esc>: call GetVWD()<CR>
