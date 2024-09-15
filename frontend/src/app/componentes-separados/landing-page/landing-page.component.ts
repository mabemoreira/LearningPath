import { ChangeDetectionStrategy, Component, Input } from "@angular/core";
@Component({
  selector: "app-landing-page",
  templateUrl: "./landing-page.component.html",
  styleUrls: ["./landing-page.component.scss"],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LandingPageComponent {}
