copy them to vimrc 

translate en to zh_CN plugin for vim 

the nmap for normal mode 
just press ctrl-shift-k the under cursor word will be translate to chinese
nmap <silent> <c-s-K> <Esc>: call GetWD() <CR>



this keymap for a build-in doc translate you must vi visual mode and select the
word and press ctrl-shift-k
this keymap also for select specific word :
ex: endfunction
          ^
you just want to know what function mean in chinese 
go to the visual mode and select the word "function" then press c-s-t

vmap <silent> <c-s-K> <Esc>: call GetVWD()<CR>


