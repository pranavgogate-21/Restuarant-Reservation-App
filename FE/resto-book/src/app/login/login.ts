import { Component } from '@angular/core';
import { Header } from "../header/header";
import { AuthService } from '../auth-service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  imports: [Header, FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {

  username: string = ""
  password: string = ""

  constructor(private auth: AuthService){
    console.log("login component is initialized")
  }

  login(){
    const data = new FormData();
    data.append("username", this.username)
    data.append("password", this.password)
    this.auth.loginUser(data).subscribe({next: (res)=>{
      console.log(res)
    }, error: (err)=>{
      console.log(err)
    }})

  }

}
