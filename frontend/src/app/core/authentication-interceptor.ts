import { HttpEvent, HttpHandlerFn, HttpRequest } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../environments/environment";


export function authenticationInterceptor(
    req: HttpRequest<unknown>,
    next: HttpHandlerFn
): Observable<HttpEvent<unknown>> {
    const authToken: null | string = localStorage.getItem(environment.AuthToken);

    if (authToken) {
        req = req.clone({headers: req.headers.set("authorization", `Token ${authToken}`)});
    }

    return next(req);
  }