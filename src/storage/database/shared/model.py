from coze_coding_dev_sdk.database import Base

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Double, ForeignKey, Integer, Numeric, PrimaryKeyConstraint, String, Table, Text, text, func
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import relationship
from typing import Optional
import datetime

from sqlalchemy.orm import Mapped, mapped_column

class HealthCheck(Base):
    __tablename__ = 'health_check'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='health_check_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))


t_pg_stat_statements = Table(
    'pg_stat_statements', Base.metadata,
    Column('userid', OID),
    Column('dbid', OID),
    Column('toplevel', Boolean),
    Column('queryid', BigInteger),
    Column('query', Text),
    Column('plans', BigInteger),
    Column('total_plan_time', Double(53)),
    Column('min_plan_time', Double(53)),
    Column('max_plan_time', Double(53)),
    Column('mean_plan_time', Double(53)),
    Column('stddev_plan_time', Double(53)),
    Column('calls', BigInteger),
    Column('total_exec_time', Double(53)),
    Column('min_exec_time', Double(53)),
    Column('max_exec_time', Double(53)),
    Column('mean_exec_time', Double(53)),
    Column('stddev_exec_time', Double(53)),
    Column('rows', BigInteger),
    Column('shared_blks_hit', BigInteger),
    Column('shared_blks_read', BigInteger),
    Column('shared_blks_dirtied', BigInteger),
    Column('shared_blks_written', BigInteger),
    Column('local_blks_hit', BigInteger),
    Column('local_blks_read', BigInteger),
    Column('local_blks_dirtied', BigInteger),
    Column('local_blks_written', BigInteger),
    Column('temp_blks_read', BigInteger),
    Column('temp_blks_written', BigInteger),
    Column('shared_blk_read_time', Double(53)),
    Column('shared_blk_write_time', Double(53)),
    Column('local_blk_read_time', Double(53)),
    Column('local_blk_write_time', Double(53)),
    Column('temp_blk_read_time', Double(53)),
    Column('temp_blk_write_time', Double(53)),
    Column('wal_records', BigInteger),
    Column('wal_fpi', BigInteger),
    Column('wal_bytes', Numeric),
    Column('jit_functions', BigInteger),
    Column('jit_generation_time', Double(53)),
    Column('jit_inlining_count', BigInteger),
    Column('jit_inlining_time', Double(53)),
    Column('jit_optimization_count', BigInteger),
    Column('jit_optimization_time', Double(53)),
    Column('jit_emission_count', BigInteger),
    Column('jit_emission_time', Double(53)),
    Column('jit_deform_count', BigInteger),
    Column('jit_deform_time', Double(53)),
    Column('stats_since', DateTime(True)),
    Column('minmax_stats_since', DateTime(True))
)


t_pg_stat_statements_info = Table(
    'pg_stat_statements_info', Base.metadata,
    Column('dealloc', BigInteger),
    Column('stats_reset', DateTime(True))
)


# 社团信息表
class Club(Base):
    __tablename__ = 'clubs'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='clubs_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="社团名称")
    club_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="社团类型（学术/文艺/运动/公益等）")
    established_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), nullable=True, comment="成立时间")
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="主管部门/指导老师")
    activities: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="核心活动内容")
    activity_time: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="活动时间")
    activity_location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="活动地点")
    requirements: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="招新要求")
    target_audience: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="适合人群")
    total_quota: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="社团总名额")
    grade1_quota: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="高一名额")
    grade2_quota: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="高二名额")
    grade3_quota: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="高三名额")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="社团简介")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment="是否招新中")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), onupdate=func.now(), nullable=True)


# 学生志愿表
class StudentApplication(Base):
    __tablename__ = 'student_applications'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='student_applications_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, comment="学号（6位数字）")
    student_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="学生姓名")
    grade: Mapped[str] = mapped_column(String(10), nullable=False, comment="年级（高一/高二/高三）")
    interest_tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="兴趣标签，JSON格式")
    preference1: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="第一志愿社团")
    preference2: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="第二志愿社团")
    preference3: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="第三志愿社团")
    priority_score: Mapped[Optional[float]] = mapped_column(Numeric(10, 4), nullable=True, comment="优先级总分")
    grade_score: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True, comment="年级基础分")
    interest_score: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True, comment="兴趣匹配分")
    random_score: Mapped[Optional[float]] = mapped_column(Numeric(10, 4), nullable=True, comment="随机小数分")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='pending', comment="状态（pending/accepted/adjusted/rejected）")
    final_club: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="最终录取的社团")
    admission_round: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="录取轮次（第几志愿/调剂）")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), onupdate=func.now(), nullable=True)


# 社团录取状态表
class AdmissionStatus(Base):
    __tablename__ = 'admission_status'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='admission_status_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    club_id: Mapped[int] = mapped_column(ForeignKey("clubs.id"), nullable=False, comment="社团ID")
    grade1_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="高一已用名额")
    grade2_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="高二已用名额")
    grade3_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="高三已用名额")
    total_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="总已用名额")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), onupdate=func.now(), nullable=True)

    # 关系
    club: Mapped["Club"] = relationship("Club")

