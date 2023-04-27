import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FirstReportComponent } from './first-report/first-report.component';
import { SecondReportComponent } from './second-report/second-report.component';

// 設計網址路徑，就可以順利的開啓自己想要的網頁
const routes: Routes = [
    { path: '', component: FirstReportComponent },
    { path: '2', component: SecondReportComponent }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
