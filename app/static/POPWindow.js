var pic_pop_window_div = document.createElement("div")
pic_pop_window_div.id = "pic-pop-window"

var pic_pop_window_item_div = document.createElement("pic-pop-window-item")
pic_pop_window_item_div.setAttribute('v-bind:pic_info', 'S_pic_info')
pic_pop_window_item_div.setAttribute('v-bind:open_window', 'openPicPopWindow')
pic_pop_window_item_div.setAttribute('v-bind:anime_style', 'anime_style')


pic_pop_window_div.appendChild(pic_pop_window_item_div)
document.body.appendChild(pic_pop_window_div)

function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

Vue.component("pic-pop-window-item", {
    template:`
<div>
    <div style="position: fixed;top: 0;left: 0;--animate-duration: 1s;
        z-index: 1052;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background-color: rgba(0, 0, 0, .6);
        display: flex;align-items: center;
        justify-content: center;" 
        v-if="open_window"
        class="animate__animated" :class="anime_style"
        @click="closeWindow()"
    >
        <i class="fas fa-times" style="position: fixed;
            top: 20px;cursor: pointer;
            right: 20px;
            color: var(--white);
            font-size: 3rem;"
            @click="closeWindow()"
        >
        </i>
        <img @click.stop :src="pic_info" style="max-width: 80vw;max-height: 80vh;"/>
    </div>
</div>
`,
    data: function () {
        return {
            
        }
    },
    props: ['pic_info','open_window', 'anime_style'],
    methods:{
        closeWindow(){
            pic_pop_window.closeWindow()
        },
    },
    computed: {
    },
})

var pic_pop_window =  new Vue({
    el: '#pic-pop-window',
    data: {
        S_pic_info : "",
        openPicPopWindow: false,
        anime_style: "",
    },
    methods:{
        setPic(S_pic_info){
            this.S_pic_info = S_pic_info
        },
        openWindow(S_pic_info=undefined){
            if (S_pic_info != undefined){
                this.setPic(S_pic_info)
            }
            this.anime_style = "animate__fadeIn"
            this.openPicPopWindow = true
        },
        closeWindow(){
            this.anime_style = "animate__fadeOut"
            setTimeout(function(){
                pic_pop_window.openPicPopWindow = false
            },1000)
        },
    },
})