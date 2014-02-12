


##NOTE:
###translate en to zh_CN plugin for vim 
----
>`nmap <silent> <c-s-K> <Esc>: call GetWD<CR>`   

>the nmap for normal mode 
>just press ctrl-shift-k the under cursor word will be translate to chinese

------
>`vmap <silent> <c-s-K> <Esc>: call GetVWD<CR>`   

>this keymap for a build-in doc translate you must in visual mode and select the
>word and press ctrl-shift-k
>this keymap also for select specific word :
>ex: endfunction
          ^
>you just want to know what function mean in chinese 
>then you will do this...
>go to the visual mode and select the word "function" then press ctrl-shift-k

------

**how to use:**   

put this in your vimrc file   

`nmap <silent> <c-s-K> <Esc>: GetWD<CR>`   

`vmap <silent> <c-s-K> <Esc>: GetVWD<CR>`   


