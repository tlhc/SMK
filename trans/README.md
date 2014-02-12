copy them to vimrc 

translate en to zh_CN plugin for vim 

the nmap for normal mode 
just press C-T the under cursor word will be translate to chinese
nmap <C-T> : call GetWD() <CR>

this for a build-in doc translate you must vi visual mode and select the
word and press C-T
noremap <silent> <C-T> <Esc>: call GetVWD()<CR>


