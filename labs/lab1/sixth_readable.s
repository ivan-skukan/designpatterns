.file	"sixth.cpp"
	.intel_syntax noprefix
	.text
	.section	.text.Base::Base(),"axG",@progbits,Base::Base(),comdat
	.align 2
	.weak	Base::Base()
	.type	Base::Base(), @function
Base::Base():
.LFB1:
	.cfi_startproc
	endbr64
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	sub	rsp, 16
	mov	QWORD PTR -8[rbp], rdi
	lea	rdx, vtable for Base[rip 16]
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR -8[rbp]
	mov	rdi, rax
	call	Base::metoda()
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1:
	.size	Base::Base(), .-Base::Base()
	.weak	Base::Base()
	.set	Base::Base(),Base::Base()
	.section	.rodata
.LC0:
	.string	"ja sam bazna implementacija!"
	.section	.text.Base::virtualnaMetoda(),"axG",@progbits,Base::virtualnaMetoda(),comdat
	.align 2
	.weak	Base::virtualnaMetoda()
	.type	Base::virtualnaMetoda(), @function
Base::virtualnaMetoda():
.LFB3:
	.cfi_startproc
	endbr64
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	sub	rsp, 16
	mov	QWORD PTR -8[rbp], rdi
	lea	rax, .LC0[rip]
	mov	rdi, rax
	call	puts@PLT
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE3:
	.size	Base::virtualnaMetoda(), .-Base::virtualnaMetoda()
	.section	.rodata
.LC1:
	.string	"Metoda kaze: "
	.section	.text.Base::metoda(),"axG",@progbits,Base::metoda(),comdat
	.align 2
	.weak	Base::metoda()
	.type	Base::metoda(), @function
Base::metoda():
.LFB4:
	.cfi_startproc
	endbr64
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	sub	rsp, 16
	mov	QWORD PTR -8[rbp], rdi
	lea	rax, .LC1[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT
	mov	rax, QWORD PTR -8[rbp]
	mov	rax, QWORD PTR [rax]
	mov	rdx, QWORD PTR [rax]
	mov	rax, QWORD PTR -8[rbp]
	mov	rdi, rax
	call	rdx
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE4:
	.size	Base::metoda(), .-Base::metoda()
	.section	.text.Derived::Derived(),"axG",@progbits,Derived::Derived(),comdat
	.align 2
	.weak	Derived::Derived()
	.type	Derived::Derived(), @function
Derived::Derived():
.LFB6:
	.cfi_startproc
	endbr64
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	sub	rsp, 16
	mov	QWORD PTR -8[rbp], rdi
	mov	rax, QWORD PTR -8[rbp]
	mov	rdi, rax
	call	Base::Base()
	lea	rdx, vtable for Derived[rip 16]
	mov	rax, QWORD PTR -8[rbp]
	mov	QWORD PTR [rax], rdx
	mov	rax, QWORD PTR -8[rbp]
	mov	rdi, rax
	call	Base::metoda()
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	Derived::Derived(), .-Derived::Derived()
	.weak	Derived::Derived()
	.set	Derived::Derived(),Derived::Derived()
	.section	.rodata
	.align 8
.LC2:
	.string	"ja sam izvedena implementacija!"
	.section	.text.Derived::virtualnaMetoda(),"axG",@progbits,Derived::virtualnaMetoda(),comdat
	.align 2
	.weak	Derived::virtualnaMetoda()
	.type	Derived::virtualnaMetoda(), @function
Derived::virtualnaMetoda():
.LFB8:
	.cfi_startproc
	endbr64
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	sub	rsp, 16
	mov	QWORD PTR -8[rbp], rdi
	lea	rax, .LC2[rip]
	mov	rdi, rax
	call	puts@PLT
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE8:
	.size	Derived::virtualnaMetoda(), .-Derived::virtualnaMetoda()
	.text
	.globl	main
	.type	main, @function
main:
.LFB9:
	.cfi_startproc
	.cfi_personality 0x9b,DW.ref.__gxx_personality_v0
	.cfi_lsda 0x1b,.LLSDA9
	endbr64
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	push	r13
	push	r12
	push	rbx
	sub	rsp, 24
	.cfi_offset 13, -24
	.cfi_offset 12, -32
	.cfi_offset 3, -40
	mov	edi, 8
.LEHB0:
	call	_Znwm@PLT
.LEHE0:
	mov	rbx, rax
	mov	r13d, 1
	mov	rdi, rbx
.LEHB1:
	call	Derived::Derived()
.LEHE1:
	mov	QWORD PTR -40[rbp], rbx
	mov	rax, QWORD PTR -40[rbp]
	mov	rdi, rax
.LEHB2:
	call	Base::metoda()
	mov	eax, 0
	jmp	.L11
.L10:
	endbr64
	mov	r12, rax
	test	r13b, r13b
	je	.L9
	mov	esi, 8
	mov	rdi, rbx
	call	_ZdlPvm@PLT
.L9:
	mov	rax, r12
	mov	rdi, rax
	call	_Unwind_Resume@PLT
.LEHE2:
.L11:
	add	rsp, 24
	pop	rbx
	pop	r12
	pop	r13
	pop	rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE9:
	.globl	__gxx_personality_v0
	.section	.gcc_except_table,"a",@progbits
.LLSDA9:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE9-.LLSDACSB9
.LLSDACSB9:
	.uleb128 .LEHB0-.LFB9
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0
	.uleb128 0
	.uleb128 .LEHB1-.LFB9
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L10-.LFB9
	.uleb128 0
	.uleb128 .LEHB2-.LFB9
	.uleb128 .LEHE2-.LEHB2
	.uleb128 0
	.uleb128 0
.LLSDACSE9:
	.text
	.size	main, .-main
	.weak	vtable for Derived
	.section	.data.rel.ro.local.vtable for Derived,"awG",@progbits,vtable for Derived,comdat
	.align 8
	.type	vtable for Derived, @object
	.size	vtable for Derived, 24
vtable for Derived:
	.quad	0
	.quad	typeinfo for Derived
	.quad	Derived::virtualnaMetoda()
	.weak	vtable for Base
	.section	.data.rel.ro.local.vtable for Base,"awG",@progbits,vtable for Base,comdat
	.align 8
	.type	vtable for Base, @object
	.size	vtable for Base, 24
vtable for Base:
	.quad	0
	.quad	typeinfo for Base
	.quad	Base::virtualnaMetoda()
	.weak	typeinfo for Derived
	.section	.data.rel.ro.typeinfo for Derived,"awG",@progbits,typeinfo for Derived,comdat
	.align 8
	.type	typeinfo for Derived, @object
	.size	typeinfo for Derived, 24
typeinfo for Derived:
	.quad	vtable for __cxxabiv1::__si_class_type_info 16
	.quad	typeinfo name for Derived
	.quad	typeinfo for Base
	.weak	typeinfo name for Derived
	.section	.rodata.typeinfo name for Derived,"aG",@progbits,typeinfo name for Derived,comdat
	.align 8
	.type	typeinfo name for Derived, @object
	.size	typeinfo name for Derived, 9
typeinfo name for Derived:
	.string	"7Derived"
	.weak	typeinfo for Base
	.section	.data.rel.ro.typeinfo for Base,"awG",@progbits,typeinfo for Base,comdat
	.align 8
	.type	typeinfo for Base, @object
	.size	typeinfo for Base, 16
typeinfo for Base:
	.quad	vtable for __cxxabiv1::__class_type_info 16
	.quad	typeinfo name for Base
	.weak	typeinfo name for Base
	.section	.rodata.typeinfo name for Base,"aG",@progbits,typeinfo name for Base,comdat
	.type	typeinfo name for Base, @object
	.size	typeinfo name for Base, 6
typeinfo name for Base:
	.string	"4Base"
	.hidden	DW.ref.__gxx_personality_v0
	.weak	DW.ref.__gxx_personality_v0
	.section	.data.rel.local.DW.ref.__gxx_personality_v0,"awG",@progbits,DW.ref.__gxx_personality_v0,comdat
	.align 8
	.type	DW.ref.__gxx_personality_v0, @object
	.size	DW.ref.__gxx_personality_v0, 8
DW.ref.__gxx_personality_v0:
	.quad	__gxx_personality_v0
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
