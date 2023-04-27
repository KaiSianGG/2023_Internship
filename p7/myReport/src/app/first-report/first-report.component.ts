import { Component } from '@angular/core';
import * as jquery from 'jquery';
declare let $:any

@Component({
    selector: 'app-first-report',
    templateUrl: './first-report.component.html',
    styleUrls: ['./first-report.component.css']
})
export class FirstReportComponent {

}
// jquery 確保文檔加載完畢才開始我們的 typescript
$(document).ready(() => {

    var reason = $('#reason').text();
    var env = $('#env').text();

    // 被提報理由不超過300字
    if (reason.length > 300) {
        // substring(0, n) 用來擷取兩個索引位置之間的字串, 假設要300字那要在n+1
        $('#reason').text(reason.substring(0, 301));
    };
    // 目前所在地概述不超過50字
    if (env.length > 50) {
        $('#env').text(env.substring(0, 51));
    };
});

