#ifndef __BFD_H_SEEN__
#define __BFD_H_SEEN__

/* Values that may appear in the flags field of a BFD.  These also
   appear in the object_flags field of the bfd_target structure, where
   they indicate the set of flags used by that backend (not all flags
   are meaningful for all object file formats) (FIXME: at the moment,
   the object_flags values have mostly just been copied from backend
   to another, and are not necessarily correct).  */

/* No flags.  */
#define BFD_NO_FLAGS    0x00

/* BFD contains relocation entries.  */
#define HAS_RELOC       0x01

/* BFD is directly executable.  */
#define EXEC_P          0x02

/* BFD has line number information (basically used for F_LNNO in a
   COFF header).  */
#define HAS_LINENO      0x04

/* BFD has debugging information.  */
#define HAS_DEBUG       0x08

/* BFD has symbols.  */
#define HAS_SYMS        0x10

/* BFD has local symbols (basically used for F_LSYMS in a COFF
   header).  */
#define HAS_LOCALS      0x20

/* BFD is a dynamic object.  */
#define DYNAMIC         0x40

/* Text section is write protected (if D_PAGED is not set, this is
   like an a.out NMAGIC file) (the linker sets this by default, but
   clears it for -r or -N).  */
#define WP_TEXT         0x80

/* BFD is dynamically paged (this is like an a.out ZMAGIC file) (the
   linker sets this by default, but clears it for -r or -n or -N).  */
#define D_PAGED         0x100

#endif