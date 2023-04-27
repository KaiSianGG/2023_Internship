import { Component } from '@angular/core';
import { greenstore } from '../assets/greenstore.const';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {
    title = 'practice';
    list = greenstore
}
