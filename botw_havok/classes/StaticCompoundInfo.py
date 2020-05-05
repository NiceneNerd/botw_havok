from typing import List, Union

from ..binary import BinaryReader, BinaryWriter
from ..binary.types import UInt32, UInt64
from ..container.util.localfixup import LocalFixup
from .base import HKBaseClass
from .common.ActorInfo import ActorInfo
from .common.ShapeInfo import ShapeInfo

if False:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class StaticCompoundInfo(HKBaseClass):
    Offset: Union[UInt32, UInt64]
    ActorInfo: List[ActorInfo]
    ShapeInfo: List[ShapeInfo]

    def __init__(self):
        super().__init__()

        self.ActorInfo = []
        self.ShapeInfo = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        ###

        if hkFile.header.pointer_size == 8:
            self.Offset = br.read_uint64()
        elif hkFile.header.pointer_size == 4:
            self.Offset = br.read_uint32()

        ActorInfoCount_offset = hkFile._assert_pointer(br)
        ActorInfoCount = hkFile._read_counter(br)

        ShapeInfoCount_offset = hkFile._assert_pointer(br)
        ShapeInfoCount = hkFile._read_counter(br)

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)
            if lfu.src == ActorInfoCount_offset:
                for _ in range(ActorInfoCount):
                    ai = ActorInfo()
                    ai.deserialize(hkFile, br, obj)
                    self.ActorInfo.append(ai)
            elif lfu.src == ShapeInfoCount_offset:
                for _ in range(ShapeInfoCount):
                    si = ShapeInfo()
                    si.deserialize(hkFile, br, obj)
                    self.ShapeInfo.append(si)
            br.step_out()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().assign_class(hkFile, obj)

        ###

        bw.reserve_uint32("EOF")

        if hkFile.header.padding_option:
            bw.write_uint32(UInt32(0))

        ActorInfoCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.ActorInfo)))

        ShapeInfoCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.ShapeInfo)))

        bw.align_to(16)

        obj.local_fixups.append(LocalFixup(ActorInfoCount_offset, bw.tell()))
        [ai.write(hkFile, bw, obj) for ai in self.ActorInfo]
        bw.align_to(16)

        obj.local_fixups.append(LocalFixup(ShapeInfoCount_offset, bw.tell()))
        [si.write(hkFile, bw, obj) for si in self.ShapeInfo]
        bw.align_to(16)

        obj.reservations.update(bw.reservations)

        ###

        super().serialize(hkFile, bw, obj)

    def asdict(self):
        d = super().asdict()
        d.update(
            {
                "ActorInfo": [ai.asdict() for ai in self.ActorInfo],
                "ShapeInfo": [si.asdict() for si in self.ShapeInfo],
            }
        )
        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.hkClass = d["hkClass"]
        inst.ActorInfo = [ActorInfo.fromdict(ai) for ai in d["ActorInfo"]]
        inst.ShapeInfo = [ShapeInfo.fromdict(si) for si in d["ShapeInfo"]]

        return inst

    def __repr__(self):
        return f"{self.__class__.__name__}({self.ActorInfo}, {self.ShapeInfo})"
