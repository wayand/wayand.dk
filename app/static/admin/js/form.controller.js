
    "use strict";
    class FormController {
        static defaultConfig = { 
            debug: false,
            ajax: false,
            requiredFields: [],
            formErrors: {},
            method: 'POST',
            action: '',
            submitSelector: 'button[type="submit"]'
        }
        
        constructor(formSelector, config) {
            this.form = document.querySelector(formSelector)
            Object.assign(this, FormController.defaultConfig, config)
            this.submit = document.querySelector(this.submitSelector)
            this.form.addEventListener("submit", this.formHandler.bind(this))

            if (!this.ajax) {
                this.form.action = this.action
                this.form.method = this.method
            }
        }

        getFieldsAsKeyValue() {
            const formData = new FormData(this.form)
            let data = {}
            for (const [key, value] of formData) {
                data[key] = value
            }
            return data
        }

        displayFieldErrors() {
            if (Object.keys(this.formErrors).length === 0) return
            for (const [fieldKey, errorMsg] of Object.entries(this.formErrors)) {
                if (fieldKey === 'csrf_token') {
                    let html = '<div class="alert alert-danger csrf_token" role="alert">' + errorMsg + '</div>'
                    this.form.querySelectorAll('.alert.alert-danger.csrf_token').forEach(el=>el?.remove())
                    this.form.insertAdjacentHTML("afterbegin", html);
                    continue
                }
                if (fieldKey === 'error') {
                    let html = '<div class="alert alert-danger error" role="alert">' + errorMsg + '</div>'
                    this.form.querySelectorAll('.alert.alert-danger.error').forEach(el=>el?.remove())
                    this.form.insertAdjacentHTML("afterbegin", html);
                    continue
                }
                this.debugLog("Displaying error msg for "+ fieldKey)
                let html = '<div class="invalid-feedback">'+errorMsg+'</div>'
                let el = document.querySelector('#'+fieldKey)
                el.parentNode.querySelector('.invalid-feedback')?.remove()
                el.classList.add('is-invalid')
                el.insertAdjacentHTML("afterend", html);
            }
        }

        resetDisplayErrors() {
            Array.from(this.form.elements).forEach(el => {
                el.classList.remove('is-invalid')
                el.parentNode.querySelector('.invalid-feedback')?.remove()
            });
        }

        debugLog(msg) {
            if (this.debug) console.log("DEBUGGING: ", msg)
        }

        validated() {
            this.resetDisplayErrors()
            const formData = this.getFieldsAsKeyValue()
            let errNo = 0 
            this.formErrors = {}
            let errors = {}
            for (const [key, value] of Object.entries(formData)) {
                if (this.requiredFields.includes(key)) {
                    this.debugLog(key+" is in requiredFields, validating..")
                    if (value.trim().length <= 0) {
                        errors[key] = key + " is required!"
                        errNo += 1
                    }
                }
            }
            if (errNo === 0) {
                return true
            } else {
                this.formErrors = errors
                return false
            }
            
        }

        async formHandler(e) {
            if (this.validated()) {
                if (this.debug) console.log('formAction', this.action, 'formMethod:', this.method)
                if (this.ajax) {
                    e.preventDefault();
                    const response = await fetch( this.action, {
                        method: this.method,
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(this.getFieldsAsKeyValue())
                    });
                    if (response.ok) {
                        const responseJson = await response.text();
                        if (this.debug) console.log('ok::::responseJson', responseJson)
                        Swal.fire({
                            icon: 'success',
                            toast: true,
                            position: 'top-end',
                            title: 'Saved',
                            timer: 3000,
                            timerProgressBar: true,
                            showConfirmButton: false,
                        })
                    } else {
                        const errors = await response.json();
                        this.formErrors = errors.errors
                        this.displayFieldErrors()
                        if (this.debug) console.log('errors::::responseJson', errors)
                    }
                } else {
                    console.log('Ajax', this.ajax)
                }
            } else {
                e.preventDefault();
                this.displayFieldErrors()
            }
            if (this.debug) console.log('formErrors:', this.formErrors)
            return true
        }
    }