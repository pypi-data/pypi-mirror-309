import{H as o,r as t,b as e,c as s,k as i,n as r,s as a,x as n}from"./index-xoMWIkw1.js";import"./c.QDLYM1G7.js";import{o as l,a as c}from"./c.DV-QrtSF.js";import"./c.BPhoTBgU.js";import"./c.BvwJ69Nz.js";import"./c.Pbr0tA_L.js";import"./c.DImmxtcL.js";import"./c.C0FxBLJt.js";import"./c.BZ90ATHi.js";let p=class extends a{constructor(){super(...arguments),this.downloadFactoryFirmware=!0}render(){return n`
      <esphome-process-dialog
        .heading=${`Download ${this.configuration}`}
        .type=${"compile"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${void 0===this._result?"":0===this._result?n`
                <mwc-button
                  slot="secondaryAction"
                  label="Download"
                  @click=${this._handleDownload}
                ></mwc-button>
              `:n`
                <mwc-button
                  slot="secondaryAction"
                  dialogAction="close"
                  label="Retry"
                  @click=${this._handleRetry}
                ></mwc-button>
              `}
      </esphome-process-dialog>
    `}_handleProcessDone(o){this._result=o.detail,0===o.detail&&l(this.configuration,this.platformSupportsWebSerial)}_handleDownload(){l(this.configuration,this.platformSupportsWebSerial)}_handleRetry(){c(this.configuration,this.platformSupportsWebSerial)}_handleClose(){this.parentNode.removeChild(this)}};p.styles=[o,t`
      a {
        text-decoration: none;
      }
    `],e([s()],p.prototype,"configuration",void 0),e([s()],p.prototype,"platformSupportsWebSerial",void 0),e([s()],p.prototype,"downloadFactoryFirmware",void 0),e([i()],p.prototype,"_result",void 0),p=e([r("esphome-compile-dialog")],p);
//# sourceMappingURL=c.B0REHsPq.js.map
