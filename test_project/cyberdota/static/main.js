var data = new Vue({
        el: '#data',
        data: {
            button_class: "btn btn-succes",
            a: "",
            clicked: 'false',
            pid: document.getElementById("idha"),
            tid:  document.getElementById("tidha"),
        },
        methods: {
            invite: function() {
                var xmlhttp = new XMLHttpRequest();
                xmlhttp.onreadystatechange = function() {
                    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                            var myObj = JSON.parse(xmlhttp.responseText);
                            data.$notify({
                              title: 'Invite',
                              message: 'You just invited a player!',
                              type: 'success',
                              class: 'bg-text-primary'
                            });
                            data.button_class = 'btn btn-success disabled'
                        };
                    } 
                data.pid = data.pid.textContent;
                data.tid = data.tid.textContent;                       
                xmlhttp.open("GET", `http://127.0.0.1:8090/api/team_invite/${data.tid}/${data.pid}`, true);
                xmlhttp.send();
                xmlhttp.readyState = 4;                    
            }
        }
    });


Vue.component('navigation', {
    template: `
            <el-menu
              class="el-menu-demo"
              mode="horizontal"
              @select="handleSelect"
              background-color="#212529"
              text-color="#6c757d"
              active-text-color="#409EFF">
              <el-menu-item @click = "home" index="0" style="font-size: 32px; color: white"><a>TM</a></el-menu-item>
              <el-menu-item @click = "home" index="1" style="font-size: 16px"> <i class="fas fa-home icons" style="color: #409EFF"></i> <a class="navlink" style="text-decoration: none; height: 30px" href="http://127.0.0.1:8090/main_menu">Home</a></el-menu-item>
              <el-menu-item @click = "profile" index="2" style="font-size: 16px"> <i class="fas fa-user" style="color: #409EFF"></i> <a class="navlink" style="text-decoration: none" href="http://127.0.0.1:8090/main"><span>Profile</span></a></el-menu-item>
              <el-menu-item @click = "search" index="3" style="font-size: 16px"> <i class="fas fa-search" style="color: #409EFF"></i> <a class="navlink" style="text-decoration: none" href="http://127.0.0.1:8090/search"><span>Search</span></a></el-menu-item>
              <el-menu-item @click = "exit" index="4" style="font-size: 16px; color:#F56C6C"> <a class="navlink" style="text-decoration: none" href="http://127.0.0.1:8090/exit"><span>Exit</span></a></el-menu-item>
            </el-menu>
                `,
    methods: {
                handleSelect(key, keyPath) {
                    console.log(key, keyPath);
                  },
                  home: function(){
                    window.location.replace("http://127.0.0.1:8090/welcome")
                  },
                  profile: function(){
                    window.location.replace("http://127.0.0.1:8090/main")
                  },
                  search: function(){
                    window.location.replace("http://127.0.0.1:8090/search")
                  },
                  exit: function(){
                    window.location.replace("http://127.0.0.1:8090/exit")
                  }         
    }            
}); 

            var nav = new Vue({
                el: '#b',
            })    