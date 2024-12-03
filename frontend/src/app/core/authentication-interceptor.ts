import { HttpEvent, HttpHandlerFn, HttpRequest } from "@angular/common/http";
import { Observable } from "rxjs";


export function authenticationInterceptor(
    req: HttpRequest<unknown>,
    next: HttpHandlerFn
): Observable<HttpEvent<unknown>> {
    const authToken: null | string = localStorage.getItem("auth-token");

    if (authToken) {
        req = req.clone({headers: req.headers.set("authorization", `Token ${authToken}`)});
    }

    return next(req);
  }