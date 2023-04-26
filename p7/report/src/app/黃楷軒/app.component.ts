import { Component } from '@angular/core';

// import jquery
declare let $: any;

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent{
    title = 'report';
}

// jquery 確保文檔加載完畢才開始我們的 typescript
$(document).ready(() => {

    var reason = $('#reason').text();
    var env = $('#env').text();
    var fMember = $('#fmember').text();
    var careStatus = $('#carestatus').text();

    // 被提報理由不超過300字
    if (reason.length > 300) {
        // substring(0, n) 用來擷取兩個索引位置之間的字串, 假設要300字那要在n+1
        $('#reason').text(reason.substring(0, 301));
    };
    // 目前所在地概述不超過50字
    if (env.length > 50) {
        $('#env').text(env.substring(0, 51));
    };
    // 家庭成員概述不超過50字
    if (fMember.length > 50) {
        $('#fmember').text(fMember.substring(0, 51));
    };
    // 目前關懷情況不超過1500字
    if (careStatus.length > 1500) {
        $('#carestatus').text(careStatus.substring(0, 1501));
    };

});
