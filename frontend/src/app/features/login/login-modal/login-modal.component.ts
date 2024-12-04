import { CommonModule } from '@angular/common';
import { Component, ViewEncapsulation } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import {
  MatDialogRef,
  MatDialogContent,
  MatDialogTitle,
  MatDialogActions,
} from '@angular/material/dialog';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faCircleCheck } from '@fortawesome/free-solid-svg-icons';
import { LoginService } from '../../../shared/services/login.service';
import {
  FormGroup,
  FormControl,
  Validators,
  AbstractControl,
  ValidationErrors,
  ReactiveFormsModule
} from '@angular/forms'
import { environment } from '../../../../environments/environment';
import { UserService } from '../../../shared/services/user.service';

@Component({
  selector: 'app-login-modal',
  standalone: true,
  imports: [
    CommonModule,
    FontAwesomeModule,
    MatDialogContent,
    MatDialogTitle,
    MatDialogActions,
    MatButtonModule,
    ReactiveFormsModule
  ],
  templateUrl: './login-modal.component.html',
  styleUrl: './login-modal.component.css',
  encapsulation: ViewEncapsulation.None
})
export class LoginModalComponent {
  public context: "account-creation" | "login" | "account-created" = 'login';
  public faCircleCheck = faCircleCheck;
  public userInformationForm: FormGroup = new FormGroup({
    username: new FormControl(null),
    password: new FormControl(null),
    passwordCheck: new FormControl(null)
  });
  public formErrors: string | null = null;

  private passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?:([0-9a-zA-Z])(?!\1)){8,}$/;
  private formValidators = {
    'login': {
      'username': [Validators.required],
      'password': [Validators.required],
      'passwordCheck': []
    },
    'account-creation': {
      'username': [
        (control: AbstractControl): ValidationErrors | null => {
          if (control.value) {
            return null; 
          }
          return {
            error: 'Campo obrigatório!'
          }
        }
      ],
      'password': [
        (control: AbstractControl): ValidationErrors | null => {
          if (
            control.value &&
            control.value.length >= 8 &&
            !Validators.pattern(this.passwordPattern)(control)
          ) {
            return null; 
          }
          return {
            error: `
              A senha deve ter no mínimo 8 caracteres, sendo ao menos:</br>
              <ul>
                <li>uma letra minúscula;</li>
                <li>uma letra minúscula; e</li>
                <li>um dígito.</li>
              </ul>
            `
          }
        }
      ],
      'passwordCheck': [
        Validators.required,
        (control: AbstractControl): ValidationErrors | null => {
          const password: string | null = control.parent?.get('password')?.value;
          const passwordCheck: string | null = control.value;
          if (password && password === passwordCheck) {
            return null;
          }
          return {
            error: 'As senhas estão diferentes!'
          };
        }
      ],
    },
    'account-created': {
      'username': [],
      'password': [],
      'passwordCheck': [],
    },
  };

  constructor(
    private dialogRef: MatDialogRef<LoginModalComponent>,
    private loginService: LoginService,
    private userService: UserService,
  ) {
    this.changeContext(this.context);
  }

  changeContext(context: "account-creation" | "login" | "account-created") {
    this.context = context;
    this.formErrors = null;
    this.userInformationForm.get('username')?.setValidators(
      this.formValidators[context]['username'],
    );
    this.userInformationForm.get('username')?.updateValueAndValidity();
    this.userInformationForm.get('password')?.setValidators(
      this.formValidators[context]['password'],
    );
    this.userInformationForm.get('password')?.updateValueAndValidity();
    this.userInformationForm.get('passwordCheck')?.setValidators(
      this.formValidators[context]['passwordCheck'],
    );
    this.userInformationForm.get('passwordCheck')?.updateValueAndValidity();
  }

  login() {
    this.loginService.login(
      this.userInformationForm.get('username')?.value,
      this.userInformationForm.get('password')?.value
    ).subscribe({
      next: (response: {token: string}) => {
        localStorage.setItem(environment.AuthToken, response.token);
        this.dialogRef.close();
        return true;
      },
      error: (err: {details: string}) => {
        this.formErrors = err.details;
      }
    });
  }

  createAccount() {
    this.userService.createUser(
      this.userInformationForm.get('username')?.value,
      this.userInformationForm.get('password')?.value
    ).subscribe({
      next: _ => {
        this.changeContext('account-created');
        return true;
      },
      error: (err: {details: string}) => {
        this.formErrors = err.details;
      }
    });
  }
}
